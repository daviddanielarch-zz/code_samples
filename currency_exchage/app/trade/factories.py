from decimal import Decimal

import factory

from trade.models import Trade
from trade.utils import pk_to_id


class TradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trade

    id = factory.Sequence(lambda n: pk_to_id(n + 1))  # Database pks start at 1
    rate = factory.Sequence(lambda n: Decimal(str(n)))
    sell_currency = factory.Faker('currency_code')
    buy_currency = factory.Faker('currency_code')
    sell_amount = factory.Sequence(lambda n: Decimal(str(n)))
    buy_amount = factory.Sequence(lambda n: Decimal(str(n)))

