import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mnogomoloka.ru"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')

all_links = soup.find_all('a', href=True)

internal_links = set()

for link in all_links:
    href = link['href']
    if href.startswith('/'):
        full_url = BASE_URL + href
        internal_links.add(full_url)
        print(f"Найдена ссылка: {link.text.strip():30} -> {full_url}")

print(f"\nВсего найдено внутренних ссылок: {len(internal_links)}")

with open('all_pages.txt', 'w', encoding='utf-8') as f:
    for url in sorted(internal_links):
        f.write(url + '\n')

print("Список сохранен в all_pages.txt")