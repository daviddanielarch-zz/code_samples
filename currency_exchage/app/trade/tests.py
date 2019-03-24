from decimal import Decimal
from unittest import mock
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from trade.factories import TradeFactory
from trade.fixer_api import get_rate, CurrencyExchangeAPIError
from trade.models import Trade, DECIMAL_PLACES
from trade.utils import round_decimal, pk_to_id, UID_MAX_REPR_VALUE


class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code


class TestPkToUID(TestCase):
    def test_initial_convertion(self):
        self.assertEqual(pk_to_id(1), 'TR0000001')

    def test_max_number_convertion(self):
        self.assertEqual(pk_to_id(UID_MAX_REPR_VALUE), 'TRZZZZZZZ')

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            pk_to_id(-1)

    def test_overflow(self):
        with self.assertRaises(ValueError):
            pk_to_id(UID_MAX_REPR_VALUE + 1)


class TestDecimalRounding(TestCase):
    def test_rounding(self):
        number = '10.{}'.format(''.zfill(DECIMAL_PLACES + 4))
        expected_number = '10.{}'.format(''.zfill(DECIMAL_PLACES))
        self.assertEqual(round_decimal(Decimal(number), DECIMAL_PLACES), Decimal(expected_number))


class TestFixerAPI(TestCase):
    def setUp(self):
        patcher = mock.patch("requests.get")
        self.fake_requests = patcher.start()
        self.addCleanup(patcher.stop)
        response = MockResponse('{"success":true,"timestamp":1553079185,"base":"EUR","date":"2019-03-20","rates":{"USD":1.135183,"EUR":1,"ARS":45.998754}}', 200)
        self.fake_requests.side_effect = [response]

    def test_get_exchange_rate(self):
        rate = get_rate('USD', 'ARS')
        self.assertEqual(rate, Decimal('40.52100322150701693030991479'))

    def test_non_200_api_response(self):
        self.fake_requests.side_effect = [MockResponse('', 403)]
        with self.assertRaises(CurrencyExchangeAPIError):
            get_rate('USD', 'ARS')

    def test_wrong_api_response_format(self):
        self.fake_requests.side_effect = [MockResponse('{}', 200)]
        with self.assertRaises(CurrencyExchangeAPIError):
            get_rate('USD', 'ARS')


class TestListTrades(APITestCase):
    def setUp(self):
        self.url = reverse('trade-api')
        TradeFactory.reset_sequence(0)
        for x in range(0, 10):
            TradeFactory()

    def test_simple_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(len(content), 10)

    def test_trades_are_ordered_by_date(self):
        content = self.client.get(self.url).json()
        first_trade = content[0]
        self.assertEqual(first_trade['id'], 'TR000000A')


class TestCreateTrade(APITestCase):
    def setUp(self):
        self.url = reverse('trade-api')
        patcher = mock.patch("requests.get")
        self.fake_requests = patcher.start()
        self.addCleanup(patcher.stop)
        response = MockResponse('{"success":true,"timestamp":1553079185,"base":"EUR","date":"2019-03-20","rates":{"USD":1.135183,"EUR":1,"ARS":45.998754}}', 200)
        self.fake_requests.return_value = response

    def test_simple_create(self):
        response = self.client.post(self.url, {'sell_currency': 'USD', 'sell_amount': "100", 'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trade.objects.count(), 1)
        new_trade = Trade.objects.get()
        self.assertEqual(new_trade.sell_currency, 'USD')
        self.assertEqual(new_trade.buy_currency, 'ARS')
        self.assertEqual(new_trade.sell_amount, Decimal('100'))
        self.assertEqual(new_trade.id, 'TR0000001')

    def test_trades_created_have_consecutive_uids(self):
        self.client.post(self.url, {'sell_currency': 'USD', 'sell_amount': "100", 'buy_currency': 'ARS'})
        trade = Trade.objects.all()[0]
        self.assertEqual(trade.id, 'TR0000001')

        self.client.post(self.url, {'sell_currency': 'USD', 'sell_amount': "100", 'buy_currency': 'ARS'})
        trade = Trade.objects.all()[0]
        self.assertEqual(trade.id, 'TR0000002')

    def test_sell_currency_is_required(self):
        response = self.client.post(self.url, {'sell_amount': "100", 'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('sell_currency', response.data)

    def test_buy_currency_is_required(self):
        response = self.client.post(self.url, {'sell_amount': "100", 'sell_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('buy_currency', response.data)

    def test_sell_amount_is_required(self):
        response = self.client.post(self.url, {'sell_currency': "USD", 'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('sell_amount', response.data)

    def test_cant_create_new_trade_if_max_id_was_reached(self):
        TradeFactory(uid=UID_MAX_REPR_VALUE)
        response = self.client.post(self.url, {'sell_currency': 'USD', 'sell_amount': "100", 'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)


class TestGetRate(APITestCase):
    def setUp(self):
        self.url = reverse('get-rate')
        patcher = mock.patch("trade.views.get_rate")
        self.fake_get_rate = patcher.start()
        self.addCleanup(patcher.stop)
        self.fake_get_rate.return_value = Decimal('1.2')

    def test_simple_get_rate(self):
        response = self.client.get(self.url, {'sell_currency': 'USD', 'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, 200)

        content = response.json()
        self.assertEqual(content, {'rate': 1.2})

    def test_missing_sell_currency(self):
        response = self.client.get(self.url, {'buy_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)

    def test_missing_buy_currency(self):
        response = self.client.get(self.url, {'sell_currency': 'ARS'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_sell_currency(self):
        response = self.client.get(self.url, {'sell_currency': 'ZZZ'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_buy_currency(self):
        response = self.client.get(self.url, {'buy_currency': 'ZZZ'})
        self.assertEqual(response.status_code, 400)
