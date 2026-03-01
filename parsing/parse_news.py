from utils import get_page, save_html, save_json, make_full_url, extract_text_content

def get_all_news():
    """Парсит все новости с сайта"""

    print("=" * 50)
    print("ПАРСИНГ НОВОСТЕЙ")
    print("=" * 50)

    news_list_url = make_full_url("/news/")
    print(f"Загружаем список новостей: {news_list_url}")

    soup = get_page(news_list_url)
    if not soup:
        return []

    save_html(soup, "news_list")

    all_links = soup.find_all('a', href=True)

    news_urls = set()
    news_titles = {}

    for link in all_links:
        href = link['href']
        if href.startswith('/news/') and href != '/news/' and href != '/news':
            parts = href.split('/')
            if len(parts) >= 3 and parts[2].isdigit():
                full_url = make_full_url(href)
                news_urls.add(full_url)
                if link.text.strip():
                    news_titles[full_url] = link.text.strip()

    print(f"Найдено ссылок на новости: {len(news_urls)}")

    news_data = []

    for i, news_url in enumerate(sorted(news_urls), 1):
        print(f"\nНовость {i}/{len(news_urls)}")
        print(f"URL: {news_url}")

        soup = get_page(news_url)
        if not soup:
            continue

        news_id = news_url.split('/')[-2]
        save_html(soup, f"news_{news_id}")

        content = extract_text_content(soup, news_url)

        date = None
        date_elem = (soup.find('time') or
                     soup.find(class_='date') or
                     soup.find(class_='news-date'))
        if date_elem:
            date = date_elem.text.strip()

        img = soup.find('img')
        image_url = None
        if img and img.get('src'):
            src = img['src']
            image_url = make_full_url(src) if src.startswith('/') else src

        title = news_titles.get(news_url, content['title'])

        news_item = {
            'id': news_id,
            'url': news_url,
            'title': title,
            'full_title': content['title'],
            'date': date,
            'content': content['content'],
            'preview': content['content'][:300] + '...' if len(content['content']) > 300 else content['content'],
            'image': image_url
        }

        news_data.append(news_item)
        print(f"Заголовок: {title}")
        print(f"Дата: {date if date else 'не найдена'}")
        print(f"Длина контента: {len(content['content'])} символов")

    save_json(news_data, 'news.json')

    print("\n" + "=" * 50)
    print(f"Обработано новостей: {len(news_data)}")
    print("=" * 50)

    return news_data


if __name__ == '__main__':
    get_all_news()