from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.settings import CURRENCIES
from trade.fixer_api import get_rate
from trade.models import Trade, DECIMAL_PLACES

from trade.utils import pk_to_id, UID_MAX_REPR_VALUE, round_decimal


class TradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('sell_currency', 'sell_amount', 'buy_currency')

    def create(self, validated_data):
        trade = Trade(**validated_data)
        next_pk = get_next_pk()
        if next_pk > UID_MAX_REPR_VALUE:
            raise ValidationError("Can't create more trades")

        trade.id = pk_to_id(next_pk)
        rate = get_rate(trade.sell_currency, trade.buy_currency)
        trade.sell_amount = trade.sell_amount
        trade.buy_amount = round_decimal(trade.sell_amount * rate, DECIMAL_PLACES)
        trade.rate = round_decimal(rate, DECIMAL_PLACES)
        trade.save()
        return trade


class TradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked')


class RateSerializer(serializers.Serializer):
    sell_currency = serializers.ChoiceField(choices=CURRENCIES, required=True)
    buy_currency = serializers.ChoiceField(choices=CURRENCIES, required=True)


def get_next_pk():
    last_trade = Trade.objects.first()
    last_trade_pk = last_trade.pk + 1 if last_trade else 1
    return last_trade_pk
