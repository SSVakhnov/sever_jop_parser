import requests

from django.http import JsonResponse
from django.shortcuts import render

from bs4 import BeautifulSoup

from apps.scraper.cosntants.enums import ParseLink
from apps.scraper.models import Vacancy
from apps.scraper.services.parser_dou import DouParser

__all__ = [
    'index_view'
]



def index_view(request, *args, **kwargs):
    v = Vacancy.objects.none()
    return render(request, 'index.html')


def debug_view(request, *args, **kwargs):
    """ Запускает прцесс парсинка DOu """
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    #     'Referer': ParseLink.DOU.value,
    # }
    # vacancy_html = requests.get(ParseLink.DOU.value, headers=headers)
    # page = BeautifulSoup(vacancy_html.text, 'html.parser')
    # # получаем значение вапкансий всего
    # vacancies_amount = page.find('h1').string.split()[0]
    #
    # csrf_token = page.find_all(attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
    # # получаем через json все вакансии
    # data = {
    #     'csrfmiddlewaretoken': csrf_token,
    #     # 'count': vacancies_amount
    #     'count': 40
    # }
    # headers['csrfmiddlewaretoken'] = csrf_token
    # cookies = {
    #     'csrftoken': csrf_token,
    #     'lang': 'ru'
    # }
    #
    # # Вытягиваем список вакансий
    # vacancies_all = requests.post(ParseLink.DOU.value + '/xhr-load/', data=data, headers=headers, cookies=cookies)
    # json = vacancies_all.json()
    # answer = BeautifulSoup(json['html'], 'html.parser')
    # vacancy_html_list = answer.find_all('div', class_='vacancy')
    #
    # # разбираем вакансию на состовляющие
    # count = 1
    # for vacancy in vacancy_html_list:
    #     if count == 1:
    #         print(vacancy.prettify())
    #         vacancy_id = vacancy.get('_id')
    #         title = vacancy.find('a').text
    #         company_name = vacancy.find('a', class_='company').text
    #         cities = vacancy.find('span', class_='cities').text
    #         short_description = vacancy.find('div', class_='sh-info').text
    #         print(f'id: {vacancy_id}, title: {title}, company: {company_name}, cities: {cities}, description: {short_description}')
    #     count += 1
    #
    # # Подробная выборка вакансии
    # link = vacancy_html_list[0].find('a').get('href')
    # vacancy_detailed_html = requests.get(link, headers=headers)
    # vacancy_detailed_html = BeautifulSoup(vacancy_detailed_html.text, 'html.parser')
    # detailed_description = vacancy_detailed_html.find('div', class_='vacancy-section')
    # print(detailed_description.text)
    # return render(request, 'base.html', {'result': answer})

    dou_parser = DouParser()
    dou_parser.run()

    return render(request, 'base.html', {})
