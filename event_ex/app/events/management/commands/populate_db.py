import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = 'Populate db with events'

    def handle(self, *args, **options):
        user = User.objects.create(username='admin', password='admin12345')
        now = datetime.datetime.utcnow()
        events = []
        for x in range(10000):
            events.append(Event(title='title{}'.format(x),
                                description='description{}'.format(x),
                                date=now + datetime.timedelta(days=x),
                                owner=user))

        Event.objects.bulk_create(events)
