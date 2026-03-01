import requests
import time
import json
from bs4 import BeautifulSoup
from config import HEADERS, DELAY, BASE_URL


def get_page(url):
    """Загружает страницу и возвращает BeautifulSoup объект"""
    print(f"📥 Загружаю: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        time.sleep(DELAY)
        soup = BeautifulSoup(response.text, 'lxml')
        soup.url = url
        return soup
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None


def save_html(soup, filename):
    """Сохраняет HTML для отладки"""
    if soup:
        with open(f'debug_{filename}.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))


def extract_text_content(soup, url=""):
    """Извлекает текстовое содержимое страницы"""
    if not soup:
        return {'title': '', 'content': '', 'url': url}

    # Заголовок
    title = soup.find('h1')
    title_text = title.text.strip() if title else ''


    content = (soup.find('div', class_='content') or
               soup.find('article') or
               soup.find('main') or
               soup.find('div', class_='page-content'))

    if content:
        content_text = content.text.strip()
    else:
        content_text = ' '.join(soup.body.stripped_strings) if soup.body else ''

    return {
        'title': title_text,
        'content': content_text,
        'url': url
    }


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {filename}")


def make_full_url(path):
    """Преобразует относительный путь в полный URL"""
    if path.startswith('http'):
        return path
    if path.startswith('/'):
        return BASE_URL + path
    return BASE_URL + '/' + path