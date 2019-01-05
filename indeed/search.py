from collections import defaultdict

from utils import combinations


def index_jobs(jobs):
    index = {'title': defaultdict(list),
             'company': defaultdict(list)
             }
    for job in jobs:
        title_combinations = combinations(job['title'].lower())
        company_combinations = combinations(job['company'].lower())
        for title in title_combinations:
            index['title'][title].append(job['id'])

        for company in company_combinations:
            index['company'][company].append(job['id'])

    return index


def search_jobs(index, query):
    query_string = query.lower()
    results = []
    if query_string in index['title']:
        results += (elem for elem in index['title'][query_string])

    if query_string in index['company']:
        results += (elem for elem in index['company'][query_string])

    for result in results:
        yield result
