import json
from decimal import Decimal

import requests

from app.settings import FIXER_URL, FIXER_ACCESS_KEY


class CurrencyExchangeAPIError(Exception):
    pass


def get_rate(sell_currency, buy_currency):
    """
    Get the exchange rate for the @sell_currency and @buy_currency pair
    @sell_currency: Currency to sell ISO 4217 code
    @buy_currency: Currency to buy ISO 4217 code

    Returns the exchange rate between the provided currencies as a Decimal object
    Raises CurrencyExchangeAPIError if something goes wrong when communicating with the Fixer.io API
    """
    currencies = ','.join([sell_currency, buy_currency])
    response = requests.get(FIXER_URL, params={'access_key': FIXER_ACCESS_KEY, 'symbols': currencies})
    if response.status_code == 200:
        response = json.loads(response.content, parse_float=Decimal)
        if not response.get('success', False):
            raise CurrencyExchangeAPIError(response.get('error', {}).get('info', 'No error to show'))
    else:
        raise CurrencyExchangeAPIError('Something went wrong while trying to get the currencies exchange rate. Try again later')

    sell_currency_rate = response['rates'][sell_currency]
    buy_currency_rate = response['rates'][buy_currency]
    rate = Decimal("1.0") / sell_currency_rate * buy_currency_rate

    return rate
