import datetime

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, Rsvp


class TestCreateEventsAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', username='test', password='test')
        self.create_url = reverse('events-list')
        self.event = Event.objects.create(title='test', description='test', date=datetime.datetime.utcnow(), owner=self.user)
        self.edit_url = reverse('events-detail', (self.event.id,))

    def test_user_must_be_auth_to_create(self):
        """
        Ensure non authenticated users can't create events
        """
        data = {'title': 'Test title', 'description': 'Test description', 'date': '2018-10-20T10:12'}
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event(self):
        """
        Ensure we can create a new event
        """
        data = {'title': 'Test title', 'description': 'Test description', 'date': '2018-10-20T10:12'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

        event = Event.objects.last()
        self.assertEqual(event.title, 'Test title')
        self.assertEqual(event.date, datetime.datetime(2018, 10, 20, 10, 12))
        self.assertEqual(event.description, 'Test description')
        self.assertEqual(event.participants, 0)

    def test_cant_create_event_with_missing_fields(self):
        """
        Ensure we can't create a new event if data is missing
        """
        data = {'title': 'Test title', 'date': '2018-10-20T10:12'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestEditEventsAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', username='test', password='test')
        self.event = Event.objects.create(title='test', description='test', date=datetime.datetime.utcnow(), owner=self.user)
        self.edit_url = reverse('events-detail', (self.event.id,))

    def test_edit_event(self):
        """
        Ensure the owner can edit the event info
        """
        data = {'title': 'New title'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.edit_url, data=data, format='json')
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event.title, 'New title')

    def test_cant_edit_not_owned_event(self):
        """
        Ensure users other than the owner can't edit the event info
        """
        data = {'title': 'New title'}
        other_user = User.objects.create(username='test2', password='test2')
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteEventsAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', username='test', password='test')
        self.event = Event.objects.create(title='test', description='test', date=datetime.datetime.utcnow(), owner=self.user)
        self.edit_url = reverse('events-detail', (self.event.id,))

    def test_edit_event(self):
        """
        Ensure the owner of an event can delete it
        """
        data = {'title': 'New title'}
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_cant_edit_not_owned_event(self):
        """
        Ensure other user than the owner can't delete the event
        """
        data = {'title': 'New title'}
        other_user = User.objects.create(username='test2', password='test2')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRsvpAPI(APITestCase):
    def setUp(self):
        self.url = reverse('rsvp-list')
        self.user = User.objects.create(email='test@test.com')
        self.event = Event.objects.create(title='test', date=datetime.datetime.utcnow(), description='test', owner=self.user)

    def test_create_rsvp(self):
        """
        Ensure we can create a new RSVP
        """
        data = {'event': self.event.id, 'user': self.user.id}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rsvp.objects.count(), 1)

        self.event.refresh_from_db()
        rsvp = Rsvp.objects.get()
        self.assertEqual(rsvp.event, self.event)
        self.assertEqual(rsvp.user, self.user)
        self.assertEqual(self.event.participants, 1)

    def test_duplicate_rsvp_should_not_be_allowed(self):
        """
        Ensure the same user can't make the two RSVP on the same event
        """
        data = {'event': self.event.id, 'user': self.user.id}
        self.client.post(self.url, data=data, format='json')
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rsvp.objects.count(), 1)

    def test_create_rsvp_invalid_user(self):
        """
        Ensure we can't create a RSVP if the user is invalid
        """
        data = {'event': self.event.id, 'user': 1231231}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaises(Rsvp.DoesNotExist):
            Rsvp.objects.get()

    def test_create_rsvp_invalid_event(self):
        """
        Ensure we can't create a RSVP if the event is invalid
        """
        data = {'event': 213131, 'user': self.user.id}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaises(Rsvp.DoesNotExist):
            Rsvp.objects.get()


class TestDeleteRsvpAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.event = Event.objects.create(title='test', date=datetime.datetime.utcnow(), description='test', owner=self.user)
        self.rsvp = Rsvp.objects.create(user=self.user, event=self.event)
        self.url = reverse('rsvp-detail', (self.rsvp.pk,))

    def test_delete_rsvp(self):
        """
        Ensure we can delete a RSVP
        """
        self.assertEqual(self.event.participants, 1)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rsvp.objects.count(), 0)
        self.event.refresh_from_db()
        self.assertEqual(self.event.participants, 0)
