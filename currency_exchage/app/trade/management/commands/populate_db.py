from django.core.management.base import BaseCommand

from trade.factories import TradeFactory
from trade.models import Trade


class Command(BaseCommand):
    help = 'Populate db with trades'

    def handle(self, *args, **options):
        last_pk = Trade.objects.first().uid
        TradeFactory.reset_sequence(last_pk)
        for x in range(100):
            TradeFactory()
