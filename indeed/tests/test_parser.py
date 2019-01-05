from unittest import TestCase

import vcr

from parser import parse_jobs
from spider import get_single_page_jobs


class TestParser(TestCase):
    @vcr.use_cassette('setUp')
    def setUp(self):
        self.jobs = get_single_page_jobs('engineer', 'madrid')

    def test_simple(self):
        parsed_jobs = list(parse_jobs(self.jobs))
        self.assertEqual(len(parsed_jobs), 16)

        first_job = parsed_jobs[0]
        self.assertEqual(first_job['title'], 'Quality Engineer (f/m)')
        self.assertEqual(first_job['company'], 'eBay Inc.')
        self.assertEqual(first_job['url'], 'https://www.indeed.es/pagead/clk?mo=r&ad=-6NYlbfkN0AMJeVuk4ECd5K_1LfpdW7JxefdFJh_RJqhU5XMhpZ8EbjGPQC3qr2a3H3RQU1MoVnUugnkCMBFpkAhWnCSML-vt2KHTUXzqbRpDUubP1aukFBP2-VHD5sM2wXizEDxgqiuI9uS89uF5DvZ_crHfbSKRnmOTytvaIa63b9At38jMnj3KPX9V_064Kw6Pi-5Rr0WS4f8BDF-FcmgKefH4tVG-J2V7gFLm7eNkUr5ThurWvhduu3_p23w7BerusFUiabq1_i7sAlvCvB59usq2X9sCbgHh0XoS3BhgFfi7RK1QZTC9uEIm3m1okC7hPj87N7w0JBAyJ8bSgN3akaEQSxYtf6m_OSU7MsAoSV9Mz6-Gq_S8ABEqqLZOle3GvZ2fty2j3mDTxhpY4Vj3Upt09qSMs8PTMrPgIbvECxQM3bko_MY2O-gAnPZFDhQ3b-kxGfy2PmVVUl3ynMO7McQgfS6dCyST9UN8UtCVooSOLVFLj_yHtNdK4dTnGxMP4G9H44PIRKNk21GfIzGeyrojgIkJzQYLZn63VH7oZMVAn3CemhDHCmH-98Ob3_agU0V_pyatF6KoS31Bey4hTtRnc2cGzKrNadg6VOhb41Yev6-DzOmvxnq4yJy&vjs=3&p=1&sk=&fvj=0')
        self.assertEqual(first_job['id'], 'f7f0024a04bca7fe334919f448d63332')

