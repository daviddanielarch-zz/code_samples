import datetime

from django.db import models

from app.settings import CURRENCIES, MAX_DECIMAL_SELL_AMOUNT_DIGITS, DECIMAL_PLACES, MAX_DECIMAL_BUY_AMOUNT_DIGITS, \
    MAX_DECIMAL_RATE_DIGITS

CURRENCIES_CHOICES = [(x, x) for x in CURRENCIES]


class Trade(models.Model):
    id = models.CharField(max_length=9, unique=True)
    uid = models.AutoField(primary_key=True)
    sell_currency = models.CharField(max_length=3, choices=CURRENCIES_CHOICES, help_text="Currency ISO 4217 code to sell")
    sell_amount = models.DecimalField(max_digits=MAX_DECIMAL_SELL_AMOUNT_DIGITS, decimal_places=DECIMAL_PLACES,
                                      help_text="Amount to sell. Maxium is 999999999999999999999999.9999")
    buy_currency = models.CharField(max_length=3, choices=CURRENCIES_CHOICES, help_text="Currency ISO 4217 code to buy")
    buy_amount = models.DecimalField(max_digits=MAX_DECIMAL_BUY_AMOUNT_DIGITS, decimal_places=DECIMAL_PLACES)
    rate = models.DecimalField(max_digits=MAX_DECIMAL_RATE_DIGITS, decimal_places=DECIMAL_PLACES)
    date_booked = models.DateTimeField(auto_now=datetime.datetime.utcnow())

    class Meta:
        ordering = ('-date_booked', )
