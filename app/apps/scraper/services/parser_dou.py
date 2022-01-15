"""
This file realise dou vacancy parsing
"""
from typing import List, Union

import requests
from bs4 import BeautifulSoup

from apps.scraper.cosntants.enums import ParseLink

__all__ = [
    'DouParser'
]

from apps.scraper.helpers.parser_helper import get_safe_html_text

from apps.scraper.models import Vacancy


class DouParser:
    def __init__(self):
        self.link = ParseLink.DOU.value
        self.vacancies_pages = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Referer': self.link,
        }
        self.cookies = {
            'csrftoken': '',
            'lang': 'ru'
        }
        self.data = {
            'csrfmiddlewaretoken': '',
            'num': 20
        }
        self.vacancies_amount = 0
        self._csrf_token = ''

    def _update_csrf_token(self, bs_page):
        self._csrf_token = bs_page.find_all(attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
        self.headers['csrfmiddlewaretoken'] = self._csrf_token
        self.cookies['csrftoken'] = self._csrf_token
        self.data['csrfmiddlewaretoken'] = self._csrf_token

        return self._csrf_token

    def _vacancy_amount(self, bs_page):
        return bs_page.find('h1').string.split()[0]

    def _update_vacancy_amount(self):
        vacancies_page = self.get_first_vacancy_page()
        self.vacancies_amount = vacancies_page.find('h1').string.split()[0]

    def get_first_vacancy_page(self):
        vacancies_page = requests.get(self.link, headers=self.headers, cookies=self.cookies)
        vacancies_page = BeautifulSoup(vacancies_page.text, 'html.parser')
        self._update_csrf_token(vacancies_page)

        return vacancies_page

    def _append_vacancy_list_html(self, vacancies_page):
        vacancies_html_list = vacancies_page.find_all('div', class_='vacancy')
        self.vacancies_pages.append(vacancies_html_list)

    def _get_next_page(self):
        vacancies_page = requests.post(
            self.link + '/xhr-load/',
            data=self.data,
            headers=self.headers,
            cookies=self.cookies
        )
        json = vacancies_page.json()
        self.data['num'] += json['num']
        return BeautifulSoup(json['html'], 'html.parser')

    def _get_salary_range(self, salary_string) -> (Union[int, None], Union[int, None]):
        split_symbol = '–'

        if not salary_string:
            return None, None

        if '$' in salary_string:
            salary_string = salary_string.replace('$', '')

        if split_symbol in salary_string:
            salary_values = salary_string.split(split_symbol, maxsplit=2)
            return int(salary_values[0]), int(salary_values[1])

        return None, None

    def _get_is_remote(self, cities) -> bool:
        return 'удаленно' in cities

    def _get_short_vacancy_info(self, vacancy_html):
        """ Получает html экземпляр вакансии и вытянивает из него необходимые данные """
        vacancy_id = vacancy_html.get('_id')
        title = get_safe_html_text(vacancy_html.find('a'))
        company_name = get_safe_html_text(vacancy_html.find('a', class_='company'))
        cities = get_safe_html_text(vacancy_html.find('span', class_='cities'))
        is_remote = self._get_is_remote(cities)
        short_description = get_safe_html_text(vacancy_html.find('div', class_='sh-info'))
        salary = get_safe_html_text(vacancy_html.find('span', class_='salary'))
        salary_min, salary_max = self._get_salary_range(salary)

        return Vacancy(
            header=title,
            short_description=short_description,
            company_name=company_name,
            city=cities,
            salary_min=salary_min,
            salary_max=salary_max,
            is_remote=is_remote,
        )

    def get_vacancies_info(self):
        """ Записывает все значения из списка спаршенных вакансий и создает их в БД """
        parsed_vacancies = []
        for vacancies_page in self.vacancies_pages:
            for vacancy_html in vacancies_page:
                parsed_vacancies.append(self._get_short_vacancy_info(vacancy_html))

        Vacancy.objects.bulk_create(parsed_vacancies)

    def run(self):
        """ Инициализирует работу парсера """
        Vacancy.objects.all().delete()
        vacancies_page = self.get_first_vacancy_page()
        self._append_vacancy_list_html(vacancies_page)
        self._update_vacancy_amount()

        # делать пока не вытяну все вакансии
        # while int(self.data['num']) < int(self.vacancies_amount):
        #     vacancies_html = self._get_next_page()
        #     self._append_vacancy_list_html(vacancies_html)
        #     self._update_vacancy_amount()
        #     print(f'amount: {self.vacancies_amount}, count: {self.data["num"]}')

        vacancies_html = self._get_next_page()
        self._append_vacancy_list_html(vacancies_html)
        self._update_vacancy_amount()

        self.get_vacancies_info()
