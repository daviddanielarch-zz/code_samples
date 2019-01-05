import datetime

import dateparser
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic.base import View
import requests

from baseapp.settings import API_KEY

MARATHONS_URL = ''
MARATHON_RESULTS_URL = ''
RESULT_EXPAND_URL = ''

AUTH_HEADERS = {'Authorization': API_KEY, 'Accept': 'application/json'}
ELEMS_PER_PAGE = 20


def parse_time(time_string):
    return datetime.datetime.strptime(time_string, '%H:%M:%S').time()


def index(request):
    return render(request, 'index.html')


class Marathons(View):
    def get(self, request):
        marathons = requests.get(MARATHONS_URL, headers=AUTH_HEADERS).json()
        response = {'data': []}
        sorted_marathons = sorted(marathons, key=lambda m: dateparser.parse(m['date']))
        for marathon in sorted_marathons:
            marathon_data = {
                'id': int(marathon.get('id', '')),
                'name': marathon.get('name', ''),
                'date': marathon.get('date', '')
            }
            response['data'].append(marathon_data)
        return JsonResponse(response)


class MarathonResults(View):
    def get(self, request):
        marathon_id = request.GET.get('id')
        age_division_filter = request.GET.get('age_filter')
        hometown_filter = request.GET.get('hometown_filter')
        page_number = request.GET.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            return HttpResponseBadRequest()

        query = {}
        if marathon_id:
            query['marathonID'] = marathon_id

        if hometown_filter:
            query['city'] = hometown_filter

        if age_division_filter:
            query['division'] = age_division_filter

        response = requests.get(MARATHON_RESULTS_URL,
                                headers=AUTH_HEADERS,
                                params=query)
        if response.status_code != 200:
            return HttpResponseBadRequest()

        marathon_results = response.json()
        sorted_marathon_results = sorted(marathon_results, key=lambda r: parse_time(r['time']))
        marathon_results_with_positions = []
        for position, elem in enumerate(sorted_marathon_results):
            elem['place'] = position + 1
            marathon_results_with_positions.append(elem)

        pagination = Paginator(marathon_results_with_positions, ELEMS_PER_PAGE)
        page = pagination.page(page_number)

        return JsonResponse({
            'data': page.object_list,
            'current_page': page_number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'total_pages': pagination.num_pages
        })


class ResultExpand(View):
    def get(self, request):
        id = request.GET.get('id')
        expand_url = '{}/'.format(RESULT_EXPAND_URL, id)
        response = requests.get(expand_url,
                                headers=AUTH_HEADERS)
        return JsonResponse({'data': response.json()})
