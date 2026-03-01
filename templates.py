# форматирование текста

import re
from typing import Dict
from utils.helpers import clean_text
from constants import BUTTON_WEBSITE


def format_title(text: str, level: int = 1, emoji: str = None) -> str:
    if emoji:
        return f"{emoji} *{text}*" if level == 1 else f"**{text}**"
    return f"*{text}*" if level == 1 else f"**{text}**"


def extract_main_content(raw_text: str) -> str:
    """
    Очень простая функция: удаляет всё до ключевой фразы.
    """
    # Сначала очищаем от явного мусора
    text = clean_text(raw_text)

    # КЛЮЧЕВЫЕ ФРАЗЫ для каждого раздела
    start_phrases = [
        # Для истории
        'На сегодняшний день, Группа компаний',
        'В 1995 году',
        '1995 В 1995 году',

        # Для миссии
        'Наша миссия',
        'Молоко для людей!',

        # Для КСО
        'Корпоративная социальная ответственность',

        # Для здорового образа жизни
        '«Галактика» поддерживает',

        # Для экологии
        'Забота об окружающей среде — одна из основ',

        # Для космоса
        'Сотрудничество «Галактики»',

        # Для производства
        'Основой целью',

        # Для пути молока
        'Чтобы получить действительно полезное',

        # Для технологий
        'Одним из главных конкурентных преимуществ',

        # Для качества
        'Пищевое предприятие',

        # Для брендов
        'Основное направление',
        'Свежее Завтра',
        'Большая Кружка',
        'Добрята',
        'Сударыня',
        'Тёлушка',

        # Для пресс-центра
        'Обратиться в пресс-службу',

        # Для партнерам
        'Компания «Галактика» заинтересована',

        # Для клиентам
        'Офис в Санкт-Петербурге',

        # Для поставщикам
        'Такой сложный бизнес',

        # Для контактов
        'Группа компаний «Галактика» — крупный',

        # Для потребителям
        'Мы хотим, чтобы наша продукция',

        # Для офисов
        'Вы можете связаться с нами',

        # Для вопрос-ответ
        'Перед тем, как задать вопрос',

        # Для работы у нас
        'Список вакансий',

        # Для дистрибуции
        'С 1 января 2019 г.',

        # Для соглашения
        'Отправляя данные через формы'
    ]

    # Ищем любую из этих фраз
    for phrase in start_phrases:
        if phrase in text:
            # Нашли - берем всё с этого места
            start_index = text.find(phrase)
            result = text[start_index:]

            # Обрезаем до "Смотрите также" если есть
            if 'Смотрите также' in result:
                result = result[:result.find('Смотрите также')]

            return result.strip()

    # Если ничего не нашли - возвращаем текст без первых 300 символов
    if len(text) > 300:
        return text[300:]

    return text


def format_paragraph(text: str) -> str:
    return text


def format_page_with_links(title: str, content: str, page_url: str = None) -> str:
    """ Форматирует страницу с учетом ссылок """

    # Форматируем заголовок
    message = format_title(title) + "\n\n"

    # Извлекаем основной контент
    main_content = extract_main_content(content)

    # Добавляем форматирование абзацев
    main_content = format_paragraph(main_content)

    message += main_content + "\n\n"

    # Добавляем ссылку на полную версию
    if page_url:
        message += f"[🌐 {BUTTON_WEBSITE}]({page_url})"

    return message


def format_bold(text: str) -> str:
    return f"*{text}*"


def format_italic(text: str) -> str:
    return f"_{text}_"


def format_link(text: str, url: str) -> str:
    return f"[{text}]({url})"


def format_news_item(news: dict) -> str:
    date = news.get('date', 'Дата не указана')
    title = news.get('title', 'Без названия')
    content = news.get('content', '')

    main_content = extract_main_content(content)
    main_content = format_paragraph(main_content)

    message = f"📰 *{title}*\n"
    message += f"📅 {date}\n\n"
    message += main_content + "\n\n"

    return message


def format_news_preview(news: dict, index: int) -> str:
    date = news.get('date', 'Дата не указана')
    title = news.get('title', 'Без названия')

    if len(title) > 50:
        title = title[:47] + "..."

    return f"{index}. *{title}*\n   📅 {date}"


def format_brand_page(brand: dict) -> str:
    """
    Форматирует страницу бренда с сохранением всей информации о продуктах
    """
    name = brand.get('name', '')
    full_content = brand.get('full_content', '')

    # Заголовок
    message = format_title(name, emoji="🏷️") + "\n\n"

    # Очищаем текст, но сохраняем структуру
    text = clean_text(full_content)

    # Разбиваем на строки
    lines = text.split('\n')

    # Находим секцию "Продукция"
    product_section_start = -1
    for i, line in enumerate(lines):
        if 'продукция' in line.lower() or 'ассортимент' in line.lower():
            product_section_start = i
            break

    if product_section_start >= 0:
        # Добавляем текст до продукции (описание бренда)
        description = '\n'.join(lines[:product_section_start]).strip()
        if description:
            message += description + "\n\n"

        # Обрабатываем продукты
        current_category = ""
        for line in lines[product_section_start + 1:]:
            line = line.strip()
            if not line:
                continue

            line_lower = line.lower()

            # Проверяем категории продуктов
            if any(cat in line_lower for cat in ['йогурт', 'кефир', 'молоко', 'сметана', 'творог', 'коктейль']):
                if not any(word in line for word in ['%', 'г', 'мл']):
                    current_category = line
                    message += f"\n**{line}**\n"
                    continue

            # Это конкретный продукт
            if '%' in line or 'г' in line or 'мл' in line:
                message += f"  • {line}\n"
            else:
                # Если не продукт и не категория, добавляем как есть
                if line != current_category:
                    message += line + "\n"
    else:
        # Если не нашли секцию продукции, добавляем весь текст
        message += text

    return message


def format_search_results(results: dict, query: str) -> str:
    total = sum(len(v) for v in results.values())

    if total == 0:
        return f"❌ Ничего не найдено по запросу «{query}»"

    message = f"🔍 *Результаты поиска по запросу «{query}»:*\n\n"

    if results['brands']:
        message += "*🏷️ Бренды:*\n"
        for item in results['brands'][:3]:
            message += f"  • {item['name']}\n"
        if len(results['brands']) > 3:
            message += f"  ...и еще {len(results['brands']) - 3}\n"
        message += "\n"

    if results['news']:
        message += "*📰 Новости:*\n"
        for item in results['news'][:3]:
            message += f"  • {item['title']}\n"
        if len(results['news']) > 3:
            message += f"  ...и еще {len(results['news']) - 3}\n"
        message += "\n"

    if results['pages']:
        message += "*📄 Страницы:*\n"
        for item in results['pages'][:3]:
            message += f"  • {item['section']} → {item['page']}\n"
        if len(results['pages']) > 3:
            message += f"  ...и еще {len(results['pages']) - 3}\n"

    return message


def format_error_404(item_name: str) -> str:
    return f"😕 *«{item_name}»*\n\nСтраница временно недоступна. Возможно, она была удалена или перемещена."


def wrap_with_navigation(text: str, back_text: str = None) -> str:
    if back_text:
        return f"{text}\n\n{back_text}"
    return text


def format_list_item(text: str, bullet: str = "•") -> str:
    return f"  {bullet} {text}"


def format_text_page(title: str, content: str, page_url: str = None) -> str:
    """
    Форматирует обычную текстовую страницу (О компании, История, и т.д.)
    """
    # Заголовок
    message = format_title(title, emoji="📄") + "\n\n"

    # Очищаем текст (теперь clean_text добавляет переносы)
    text = clean_text(content)

    # Разбиваем на абзацы
    paragraphs = text.split('\n')
    formatted_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Если это заголовок (Наша миссия, Наши ценности)
        if any(header in para.lower() for header in ['наша миссия', 'наши ценности']):
            formatted_paragraphs.append(f"\n*{para}*\n")
        else:
            formatted_paragraphs.append(para)

    message += '\n\n'.join(formatted_paragraphs) + "\n\n"

    if page_url:
        message += format_link(f"🌐 {BUTTON_WEBSITE}", page_url)

    return message


def format_history_page(text: str, page_url: str = None) -> str:
    """
    Специальное форматирование для страницы истории
    """
    message = ""

    # Находим все годы в тексте
    years = re.findall(r'(19\d{2}|20\d{2})', text)

    if years:
        # Разбиваем текст по годам
        for i, year in enumerate(years):
            # Находим текст после года
            pattern = f"{year}\\s+(.*?)(?={years[i + 1] if i + 1 < len(years) else '$'})"
            match = re.search(pattern, text, re.DOTALL)

            if match:
                year_text = match.group(1).strip()
                message += f"\n**{year}** {year_text}\n\n"
            else:
                # Если не нашли паттерн, просто добавляем остаток текста
                parts = text.split(str(year))
                if len(parts) > i + 1:
                    message += f"\n**{year}** {parts[i + 1].strip()}\n\n"
    else:
        # Если нет годов, используем обычное форматирование
        message = text

    if page_url:
        message += f"\n{format_link(f'🌐 {BUTTON_WEBSITE}', page_url)}"

    return message


def format_news_page(news: dict) -> str:
    """
    Форматирует отдельную новость
    """
    title = news.get('title', '')
    date = news.get('date', '')
    content = news.get('content', '')

    # Заголовок с датой
    message = format_title(title, emoji="📰") + "\n"
    message += format_italic(date) + "\n\n"

    # Очищаем текст
    text = clean_text(content)

    # Разбиваем на абзацы
    paragraphs = text.split('\n')
    formatted_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Если абзац начинается с "-" или "•"
        if para.startswith('-') or para.startswith('•'):
            formatted_paragraphs.append(format_list_item(para[1:].strip()))
        else:
            formatted_paragraphs.append(para)

    message += '\n\n'.join(formatted_paragraphs)

    return message


def format_news_list(news_list: list, page: int = 0) -> str:
    """
    Форматирует список новостей
    """
    message = format_title("Последние новости", emoji="📰") + "\n\n"

    start_idx = page * 5
    for i, news in enumerate(news_list[start_idx:start_idx + 5], start=start_idx + 1):
        title = news.get('title', '')
        date = news.get('date', '')

        # Обрезаем длинный заголовок
        if len(title) > 50:
            title = title[:47] + "..."

        message += f"{i}. {format_bold(title)}\n"
        message += f"   {format_italic(date)}\n\n"

    message += format_italic("Отправьте номер новости (1, 2, 3...) чтобы прочитать полностью")

    return message


def format_contacts_page(content: str, page_url: str = None) -> str:
    """
    Форматирует страницу с контактами (офисы, телефоны)
    """
    message = format_title("Наши контакты", emoji="📞") + "\n\n"

    # Очищаем текст
    text = clean_text(content)

    # Разбиваем на строки
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Проверяем на телефон
        if re.search(r'\+7|8[ -]?\d{3}', line):
            message += format_bold(line) + "\n"

        # Проверяем на адрес
        elif any(word in line for word in ['ул.', 'г.', 'Санкт-Петербург', 'Москва']):
            message += format_italic(line) + "\n"

        # Проверяем на email
        elif '@' in line:
            message += format_link(line, f"mailto:{line}") + "\n"

        # Проверяем на ИНН
        elif 'ИНН' in line:
            message += line + "\n"

        # Обычный текст
        else:
            message += line + "\n"

        # Добавляем пустую строку после блока
        if any(word in line for word in ['Санкт-Петербург', 'Гатчина', 'Вятка']):
            message += "\n"

    if page_url:
        message += f"\n{format_link(f'🌐 {BUTTON_WEBSITE}', page_url)}"

    return message


def format_content(content_type: str, data: dict, **kwargs) -> str:
    """
    Универсальная функция для форматирования любого контента

    Параметры:
        content_type: тип контента ('page', 'brand', 'news', 'news_list', 'contacts')
        data: словарь с данными
        **kwargs: дополнительные параметры

    Примеры:
        format_content('page', page_data)
        format_content('brand', brand_data)
        format_content('news', news_data)
        format_content('news_list', {'list': news_list, 'page': 0})
    """
    if content_type == 'page':
        return format_text_page(
            title=data.get('title', ''),
            content=data.get('content', ''),
            page_url=data.get('url')
        )

    elif content_type == 'brand':
        return format_brand_page(data)

    elif content_type == 'news':
        return format_news_page(data)

    elif content_type == 'news_list':
        return format_news_list(
            news_list=data.get('list', []),
            page=data.get('page', 0)
        )

    elif content_type == 'contacts':
        return format_contacts_page(
            content=data.get('content', ''),
            page_url=data.get('url')
        )

    return ""


def debug_page_data(page_data: Dict, subsection_name: str) -> None:
    """ Отладочная функция для просмотра данных """
    print(f"\n=== DEBUG: {subsection_name} ===")
    print(f"Title: {page_data.get('title', 'Нет заголовка')}")
    print(f"URL: {page_data.get('url', 'Нет URL')}")
    content = page_data.get('content', '')
    print(f"Content length: {len(content)}")
    print(f"First 200 chars: {content[:200]}")
    print("=" * 50)