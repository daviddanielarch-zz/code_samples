import uuid

import requests
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from rest_framework import status

from tracker.views import items
from tracker.carts import Carts


class TestItemsWithExistingCart(TestCase):
    def setUp(self):
        self.carts = Carts()
        self.url = reverse(items)
        self.cart_id = str(uuid.uuid4())
        item = {'name': 'Computer', 'price': 100}
        self.carts.set_cart_item(self.cart_id, 'test-product', item)

    def tearDown(self):
        self.carts.redis.flushall()

    def test_returns_current_cart_id(self):
        response = self.client.post(self.url,
                                    data={'product_id': 'test', 'cart_id': self.cart_id},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['cart_id'], str(self.cart_id))

    def test_cookie_cart_id_has_priority(self):
        self.client.cookies.load({'cart_id': self.cart_id})
        response = self.client.post(self.url,
                                    data={'product_id': 'test', 'cart_id': 'sarasa'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['cart_id'], str(self.cart_id))

    def test_adds_new_item_to_existing_cart(self):
        response = self.client.post(self.url,
                                    data={'product_id': 'test', 'cart_id': self.cart_id},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = self.carts.get_cart_item(self.cart_id, 'test')
        self.assertEqual(item['name'], '')
        self.assertEqual(item['price'], '')

    def test_updates_item_data(self):
        response = self.client.post(self.url,
                                    data={
                                        'product_id': 'test-product',
                                        'cart_id': self.cart_id,
                                        'name': 'test',
                                        'price': 314
                                        },
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = self.carts.get_cart_item(self.cart_id, 'test-product')
        self.assertEqual(item['name'], 'test')
        self.assertEqual(item['price'], 314)

    def test_dont_overwrite_data_if_empty(self):
        response = self.client.post(self.url,
                                    data={
                                        'product_id': 'test-product',
                                        'cart_id': self.cart_id,
                                        'price': 314,
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = self.carts.get_cart_item(self.cart_id, 'test-product')
        self.assertNotEqual(item, None)
        self.assertEqual(item['name'], 'Computer')
        self.assertEqual(item['price'], 314)


class TestItemsNoPreviousCart(TestCase):
    def setUp(self):
        self.url = reverse(items)
        self.carts = Carts()

    def tearDown(self):
        self.carts.redis.flushall()

    def test_product_id_is_required(self):
        response = self.client.post(self.url, data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creates_a_new_cart_if_no_cart_id_is_passed(self):
        response = self.client.post(self.url, data={'product_id': 'test'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = self.carts.get_first_cart()
        self.assertNotEqual(cart, None)
        self.assertEqual(response.json()['cart_id'], str(cart))

    def test_sets_cart_id_cookie(self):
        response = self.client.post(self.url, data={'product_id': 'test'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = self.carts.get_first_cart()
        self.assertEqual(self.client.cookies.get('cart_id').value, str(cart))

    def test_invalid_uuid_creates_a_new_cart(self):
        response = self.client.post(self.url, data={'product_id': 'test', 'cart_id': 'asdsad'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = self.carts.get_first_cart()
        self.assertNotEqual(cart, None)
        self.assertEqual(response.json()['cart_id'], str(cart))


class IntegrationTest(LiveServerTestCase):
    def setUp(self):
        self.url = '{}{}'.format(self.live_server_url, reverse(items))
        self.carts = Carts()

    def tearDown(self):
        self.carts.redis.flushall()

    def test_basic_cart(self):
        # User adds first item, a new cart should be created
        response = requests.post(self.url, data={'product_id': 'computer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.carts.get_carts_count(), 1)

        cart_id = response.json()['cart_id']

        # User adds a new item, the previous cart should have two items now
        response = requests.post(self.url, data={'product_id': 'computer2', 'cart_id': cart_id})
        self.assertEqual(self.carts.get_carts_count(), 1)
        self.assertEqual(len(self.carts.get_cart_items(cart_id)), 2)
        self.assertEqual(response.status_code, 200)

        # User updates a item price
        response = requests.post(self.url, data={'product_id': 'computer2', 'cart_id': cart_id, 'price': 1000})
        self.assertEqual(response.status_code, 200)
        product = self.carts.get_cart_item(cart_id, 'computer2')
        self.assertEqual(product['price'], 1000)
