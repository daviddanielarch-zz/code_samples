from bs4 import BeautifulSoup

from settings import DOMAIN
from utils import get_job_id


def parse_jobs(response):
    content = BeautifulSoup(response.text, "html.parser")
    rows = content.find_all('div', {"class": "row"})
    for row in rows:
        company = row.find('span', {'class': 'company'})
        company = company.text.strip() if company else ''

        job = {
            'title': row.find('a').attrs['title'],
            'company': company,
            'url': '{}{}'.format(DOMAIN, row.find('a').attrs['href'])
        }
        job['id'] = get_job_id(job)

        yield job