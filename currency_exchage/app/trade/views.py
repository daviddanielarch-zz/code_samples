import coreapi
import coreschema
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from trade.fixer_api import get_rate, CurrencyExchangeAPIError
from trade.models import Trade, CURRENCIES, MAX_DECIMAL_SELL_AMOUNT_DIGITS, DECIMAL_PLACES
from trade.serializers import TradeListSerializer, TradeCreateSerializer, RateSerializer


class TradeAPI(ListCreateAPIView):
    """
get:
Return a list of all trades in the system

Example Python code using the requests lib:

    ```python
requests.get('http://127.0.0.1:8000/trades/')
```
### Request Response
The request response will be a `"application/json"` encoded object, with the following format:
```javascript

[{
    'id': 'TR0000001',
    'sell_currency': 'AMD',
    'sell_amount': '123.0000',
    'buy_currency': 'BIF',
    'buy_amount': '463.6609',
    'rate': '3.7696',
    'date_booked': '2019-03-23T19:48:03.654285'
 }...]
```

post:
Create a new trade

* The exchange rate will be calculated using an external provider (Fixer.io)
* Its only possible to sell up to **999999999999999999999999** units of currency
* Only **4** decimal places are supported for sell_amount

Example Python code using the requests lib:
```python
requests.post('http://127.0.0.1:8000/trades/', {'sell_currency': 'USD', 'buy_currency': 'ARS', 'sell_amount': 100})
```
    """
    queryset = Trade.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TradeListSerializer

        return TradeCreateSerializer


def home(request):
    return render(request, 'list.html')


def create_trade(request):
    return render(request, 'create.html',
                  {'currencies': [''] + CURRENCIES,
                   'max_decimal_places': DECIMAL_PLACES,
                   'max_sell_amount': 10 ** (MAX_DECIMAL_SELL_AMOUNT_DIGITS - DECIMAL_PLACES) - 1
                   }, )


class GetRate(APIView):
    schema = ManualSchema(fields=[
        coreapi.Field(
            "sell_currency",
            required=True,
            location="query",
            schema=coreschema.String(description="Currency to sell ISO 4217 code"),
        ),
        coreapi.Field(
            "buy_currency",
            required=True,
            location="query",
            schema=coreschema.String(description="Currency to buy ISO 4217 code")
        ),
    ],
        description="""Retrieve the currency exchange rate from an external provider. 

Currently supported providers:

* Fixer.io

Example Python code using the requests lib:
    
```python
requests.get('http://127.0.0.1:9000/rate/', params={'sell_currency':'USD', 'buy_currency':'ARS'})
```
    
### Request Response
The request response will be a `"application/json"` encoded object, with the following format:
```javascript
{'rate': 41.756}
```
    """)

    def get(self, request):
        serializer = RateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        sell_currency = serializer.validated_data.get('sell_currency')
        buy_currency = serializer.validated_data.get('buy_currency')

        try:
            rate = round(get_rate(sell_currency, buy_currency), 4)
            return Response({'rate': rate})

        except CurrencyExchangeAPIError as e:
            return Response(str(e), status=status.HTTP_424_FAILED_DEPENDENCY)
