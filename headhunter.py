import requests
from bs4 import BeautifulSoup

items = 20
url = f"https://hh.ru/search/vacancy?text=Python&from=suggest_post&salary=&clusters=true&area=1&no_magic=true&ored_clusters=true&search_field=name&enable_snippets=true&items_on_page={items}"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept': '*/*'
}


# Нахождение номера последней страницы
def extract_max_page():
    hh_request = requests.get(url, headers=headers)
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')

    pages = []
    paginator = hh_soup.findAll('span', {'class': 'pager-item-not-in-short-range'})

    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]


def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
    company = company.strip()
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Парсинг страницы: {page + 1}')
        result = requests.get(f'{url}&page={page}', headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.findAll('div', {'class': 'vacancy-serp-item-body__main-info'})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)
    return jobs
