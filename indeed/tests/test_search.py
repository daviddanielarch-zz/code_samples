from unittest import TestCase

import vcr

from parser import parse_jobs
from search import index_jobs, search_jobs
from spider import get_single_page_jobs


class TestIndex(TestCase):
    @vcr.use_cassette('setUp')
    def setUp(self):
        self.jobs = list(parse_jobs(get_single_page_jobs('engineer', 'madrid')))
        self.job = self.jobs[0]
        self.index = index_jobs(self.jobs)

    def test_index_is_in_lowercase(self):
        self.assertIn(self.job['title'].lower(), self.index['title'])
        self.assertIn(self.job['company'].lower(), self.index['company'])

    def test_index_substring(self):
        self.assertIn(self.job['title'].lower().split(' ')[0], self.index['title'])
        self.assertIn(self.job['company'].lower().split(' ')[0], self.index['company'])


class TestSearch(TestCase):
    @vcr.use_cassette('setUp')
    def setUp(self):
        self.jobs = list(parse_jobs(get_single_page_jobs('engineer', 'madrid')))
        self.job = self.jobs[0]
        self.index = index_jobs(self.jobs)

    def test_search_returns_id(self):
        search_results = search_jobs(self.index, self.job['company'])
        self.assertIn(self.job['id'], search_results)
