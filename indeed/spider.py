import requests

from parser import parse_jobs
from settings import DOMAIN, MAX_PAGES


def get_single_page_jobs(keywords, location, start=0):
    url = '{}/jobs'.format(DOMAIN)
    response = requests.get(url, params={'q': keywords, 'l': location, 'start': start})
    return response


def get_jobs(keywords, location, pages=MAX_PAGES):
    item_count = 1
    for x in range(0, pages):
        response = get_single_page_jobs(keywords, location, item_count)
        for job in parse_jobs(response):
            item_count += 1
            yield job

