import json
import re
import os
from typing import Dict, List, Any

SKIP_PHRASES = [
    'Заказать обратный звонок',
    'Отправить резюме',
    'Я даю согласие на обработку',
    'Соглашение',
    'Допустимые форматы:',
    'Максимальный обЪем файла:',
    'RU ENG ZH',
    'Подпишитесь на новости',
    'Получайте последние новости',
    'Горячая линия:',
    'Звонок по России бесплатный',
    'Задайте вопрос',
    'Поделиться:',
    'Наши бренды:',
    'Разработка сайта -',
    'Узнать больше',
    'Читать далее',
    'Подписаться'
]

HTML_TAGS = re.compile(r'<[^>]+>')
MULTIPLE_SPACES = re.compile(r'[ \t]+')  # Только пробелы и табуляция, НЕ переносы строк!
MULTIPLE_NEWLINES = re.compile(r'\n\s*\n\s*\n')


def load_data(data_path: str) -> Dict:
    try:
        if not os.path.exists(data_path):
            print(f"Файл {data_path} не найден!")
            return {}

        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Данные загружены из {data_path}")
        return data

    except json.JSONDecodeError as e:
        print(f"Ошибка в JSON файле: {e}")
        return {}
    except Exception as e:
        print(f"Неизвестная ошибка при загрузке данных: {e}")
        return {}


def get_section_data(data: Dict, section_name: str):
    return data.get('structure', {}).get('sections', {}).get(section_name, {})


def get_page_data(data: Dict, section_name: str, page_name: str):
    section = get_section_data(data, section_name)
    return section.get('subsections', {}).get(page_name, {})


def get_brand_data(data: Dict, brand_name: str):
    brands = data.get('brands', [])
    for brand in brands:
        if brand.get('name') == brand_name:
            return brand
    return None


def get_news(data: Dict, limit: int = None, offset: int = 0) -> List[Dict]:
    news = data.get('news', [])
    sorted_news = sorted(
        news,
        key=lambda x: x.get('date', '00.00.0000'),
        reverse=True
    )

    if limit is not None:
        return sorted_news[offset:offset + limit]
    return sorted_news


def clean_text(text: str, max_length: int = 3500):
    """
    Очищает текст от мусора и ДОБАВЛЯЕТ переносы строк для красивого форматирования
    """
    if not text:
        return ""

    # 1. Удаляем HTML-теги
    text = HTML_TAGS.sub('', text)

    # 2. Удаляем мусорные фразы
    for phrase in SKIP_PHRASES:
        text = text.replace(phrase, '')
        # Убираем лишние пробелы после удаления
        text = re.sub(r'[ \t]+', ' ', text)

    # 3. СПЕЦИАЛЬНАЯ ОБРАБОТКА ДЛЯ РАЗНЫХ ТИПОВ ТЕКСТА

    # Для "Миссия и ценности" - ищем ключевые фразы
    if 'миссия' in text.lower() or 'ценности' in text.lower():
        # Добавляем переносы перед ключевыми фразами
        text = re.sub(r'(Наша миссия)', r'\n\1', text, flags=re.IGNORECASE)
        text = re.sub(r'(Молоко для людей!)', r'\n\1\n', text, flags=re.IGNORECASE)
        text = re.sub(r'(Наши ценности)', r'\n\1', text, flags=re.IGNORECASE)

        # Разбиваем длинные списки ценностей
        text = re.sub(r'(Мы готовы делать больше)', r'\n\1', text)
        text = re.sub(r'(Мы являемся приверженцами)', r'\n\1', text)
        text = re.sub(r'(Говорим о пользе)', r'\n\1', text)
        text = re.sub(r'(Мы коммуницируем)', r'\n\1', text)
        text = re.sub(r'(Мы поощряем)', r'\n\1', text)
        text = re.sub(r'(Мы открыты)', r'\n\1', text)
        text = re.sub(r'(Мы уважаем)', r'\n\1', text)
        text = re.sub(r'(Мы отмечаем)', r'\n\1', text)
        text = re.sub(r'(Мы делимся)', r'\n\1', text)
        text = re.sub(r'(Мы слышим)', r'\n\1', text)
        text = re.sub(r'(Мы ценим)', r'\n\1', text)
        text = re.sub(r'(Мы соблюдаем)', r'\n\1', text)
        text = re.sub(r'(Мы работаем)', r'\n\1', text)
        text = re.sub(r'(Мы команда)', r'\n\1', text)
        text = re.sub(r'(Мы разделяем)', r'\n\1', text)
        text = re.sub(r'(Компания предоставляет)', r'\n\1', text)
        text = re.sub(r'(Мы имеем смелость)', r'\n\1', text)
        text = re.sub(r'(Мы толерантны)', r'\n\1', text)
        text = re.sub(r'(Договорились)', r'\n\1', text)
        text = re.sub(r'(Доводим дело)', r'\n\1', text)

    # Для истории - разбиваем по годам
    if any(year in text for year in ['1995', '2005', '2006', '2008', '2011', '2012', '2014', '2020']):
        # Добавляем перенос перед каждым годом
        text = re.sub(r'(19\d{2}|20\d{2})', r'\n\1', text)

    # Для всех текстов - разбиваем по предложениям
    # Ищем конец предложения (.!?) и добавляем перенос строки
    sentences = re.split(r'([.!?])\s+', text)
    if len(sentences) > 1:
        result = []
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                result.append(sentences[i] + sentences[i + 1])
        if sentences[-1]:
            result.append(sentences[-1])
        text = '\n'.join(result)

    # 4. Убираем повторяющиеся переносы
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

    # 5. Убираем пробелы в начале и конце
    text = text.strip()

    # 6. Обрезаем до лимита
    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def get_preview(text: str, length: int = 300):
    if not text:
        return ""

    clean = clean_text(text)
    if len(clean) > length:
        clean = clean[:length] + "..."
    return clean


def format_date(date_str: str):
    if not date_str or date_str == '00.00.0000':
        return "Дата не указана"

    try:
        day, month, year = date_str.split('.')

        months = {
            '01': 'января', '02': 'февраля', '03': 'марта',
            '04': 'апреля', '05': 'мая', '06': 'июня',
            '07': 'июля', '08': 'августа', '09': 'сентября',
            '10': 'октября', '11': 'ноября', '12': 'декабря'
        }

        month_name = months.get(month, month)
        return f"{int(day)} {month_name} {year}"

    except Exception:
        return date_str


def is_404_page(page_data: Dict):
    title = page_data.get('title', '')
    content = page_data.get('content', '')

    return (
            'Ошибка 404' in title or
            'Страница не найдена' in content[:200]
    )


def search_in_data(data: Dict, query: str):
    query = query.lower().strip()
    results = {
        'brands': [],
        'news': [],
        'pages': []
    }

    if not query:
        return results

    for brand in data.get('brands', []):
        if query in brand.get('name', '').lower():
            results['brands'].append({
                'type': 'brand',
                'name': brand['name'],
                'data': brand
            })

    for news in data.get('news', []):
        if (query in news.get('title', '').lower() or
            query in news.get('content', '').lower()[:500]):
            results['news'].append({
                'type': 'news',
                'title': news['title'],
                'date': news.get('date', ''),
                'data': news
            })

    sections = data.get('structure', {}).get('sections', {})
    for section_name, section in sections.items():
        for page_name, page in section.get('subsections', {}).items():
            if (query in page_name.lower() or
                query in page.get('title', '').lower()):
                results['pages'].append({
                    'type': 'page',
                    'section': section_name,
                    'page': page_name,
                    'title': page.get('title', page_name),
                    'data': page
                })

    return results


def get_data_statistics(data: Dict):
    stats = {
        'sections': 0,
        'subsections': 0,
        'brands': len(data.get('brands', [])),
        'news': len(data.get('news', [])),
        'other_pages': 0
    }

    sections = data.get('structure', {}).get('sections', {})
    stats['sections'] = len(sections)

    for section in sections.values():
        stats['subsections'] += len(section.get('subsections', {}))

    stats['other_pages'] = len(data.get('structure', {}).get('other_pages', {}))
    stats['total_pages'] = stats['sections'] + stats['subsections'] + stats['other_pages']

    return stats


def print_data_summary(data: Dict):
    stats = get_data_statistics(data)

    print("\n" + "=" * 50)
    print("СТАТИСТИКА ЗАГРУЖЕННЫХ ДАННЫХ")
    print("=" * 50)
    print(f"Разделов: {stats['sections']}")
    print(f"Подразделов: {stats['subsections']}")
    print(f"Брендов: {stats['brands']}")
    print(f"Новостей: {stats['news']}")
    print(f"Других страниц: {stats['other_pages']}")
    print(f"ВСЕГО СТРАНИЦ: {stats['total_pages']}")
    print(f"Последнее обновление: {data.get('site_info', {}).get('last_updated', 'неизвестно')}")
    print("=" * 50 + "\n")