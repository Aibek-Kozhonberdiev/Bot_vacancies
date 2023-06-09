import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.content if response.status_code == 200 else False

def scraper(html: str | bool, url: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='information')
        result = []
        for item in items:
            position = item.find('div', class_="jobs-item-field company").get_text(strip=True)
            Job_title = item.find('div', class_="jobs-item-field position").get_text(strip=True)
            salary = item.find('div', class_="jobs-item-field price").get_text(strip=True)
            type = item.find('div', class_="jobs-item-field type").get_text(strip=True)
            result.append(
                {
                    'position': position,
                    'Job_title': Job_title,
                    'salary': salary,
                    'type': type
                }
            )
        return result

url = 'https://devkg.com/ru'
html = get_html(url+'/jobs')
data = scraper(html=html, url=url)

def main():
    rez = []
    for item in data:
        position = item['Job_title'].replace('Должность', '')
        company = item['position'].replace('Компания', '')
        salary = item['salary'].replace('Оклад', '')
        job_type = item['type'].replace('Тип', '')

        rez.append(f"Должность: {position.strip()} 👔\nКомпания: {company.strip()} 🌐\nОклад: {salary.strip()} 💰\nТип: {job_type.strip()} 💼")
    return rez