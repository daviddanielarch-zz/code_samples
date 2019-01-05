import json

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = ''

    def json(self):
        return self.json_data


class ListMarathons(TestCase):
    def setUp(self):
        self.url = reverse('list_marathons')

    def test_marathons_return_sorted(self):
        data = [{'city': 'Gotham',
                 'country': 'US',
                 'date': '2018-04-02T23:02:26Z',
                 'id': 2,
                 'name': 'Gotham City Marathon',
                 'state': 'IL',
                 'track': []},
                {'city': 'Central',
                 'country': 'US',
                 'date': '2018-03-02T23:02:26Z',
                 'id': 3,
                 'name': 'Central City Marathon',
                 'state': 'NY',
                 'track': []}]
        with patch('requests.get', return_value=MockResponse(data, 200)):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data'][0]['id'], 3)


class ListResults(TestCase):
    def setUp(self):
        self.url = reverse('list_results')

    def test_sorted_positions(self):
        data = [{"id": 26414, "marathonID": 1, "bib": "11223344", "firstName": "Martin", "lastName": "Benvenuti", "city": "Mar del Plata", "state": "Buenos Aires", "country": "Argentina", "time": "11:22:33", "splits": [], "gender": "f", "age": 32, "division": 2},
                {"id": 26415, "marathonID": 1, "bib": "11223345", "firstName": "Martin", "lastName": "Benvenute", "city": "Mar del Plata", "state": "Buenos Aires", "country": "Argentina", "time": "1:22:33", "splits": [], "gender": "m", "age": 45, "division": 3},
                {"id": 10865, "marathonID": 1, "bib": "9953", "firstName": "Alejandro A. Sr.", "lastName": "Estevez", "city": "Mar Del Plata", "state": "", "country": "ARG", "time": "03:43:58", "splits": [], "gender": "m", "age": 57, "division": 3}]

        with patch('requests.get', return_value=MockResponse(data, 200)):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data'][0]['id'], 26415)
        self.assertEqual(json_response['data'][0]['place'], 1)
        self.assertEqual(json_response['data'][1]['id'], 10865)
        self.assertEqual(json_response['data'][1]['place'], 2)
        self.assertEqual(json_response['data'][2]['id'], 26414)
        self.assertEqual(json_response['data'][2]['place'], 3)

    def test_simple_pagination(self):
        data = [{'time': '10:10:10'} for x in range(0, 199)]
        with patch('requests.get', return_value=MockResponse(data, 200)):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['total_pages'], 10)
        self.assertEqual(json_response['has_next'], True)
        self.assertEqual(json_response['has_previous'], False)

