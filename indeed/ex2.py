from search import index_jobs, search_jobs

import pprint

from spider import get_jobs

print('Getting jobs')
jobs = list(get_jobs('engineer', 'madrid'))

print('Dumping jobs')
for job in jobs:
    pprint.pprint(job)

print('Creating index')
index = index_jobs(jobs)

print('Searching jobs with query=ebay')
matches = search_jobs(index, 'ebay')

print('Printing matching jobs ids')
print(set(list(matches)))