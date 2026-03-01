from config import SITE_STRUCTURE
from utils import get_page, save_html, save_json, make_full_url, extract_text_content


def get_all_brands():
    """Собирает все бренды из структуры и парсит их страницы"""

    print("=" * 50)
    print("ПАРСИНГ БРЕНДОВ")
    print("=" * 50)

    brands_section = SITE_STRUCTURE.get("Бренды", {})
    brand_items = brands_section.get("subsections", {})

    print(f"Найдено брендов в структуре: {len(brand_items)}")

    brands_data = []

    for brand_name, brand_path in brand_items.items():
        print(f"\nБренд: {brand_name}")
        brand_url = make_full_url(brand_path)

        soup = get_page(brand_url)
        if not soup:
            continue

        save_html(soup, f"brand_{brand_name}")

        content = extract_text_content(soup, brand_url)

        img = soup.find('img')
        image_url = None
        if img and img.get('src'):
            src = img['src']
            image_url = make_full_url(src) if src.startswith('/') else src

        brand_info = {
            'name': brand_name,
            'url': brand_url,
            'title': content['title'],
            'description': content['content'][:300] + '...' if len(content['content']) > 300 else content['content'],
            'full_content': content['content'],
            'image': image_url
        }

        brands_data.append(brand_info)
        print(f"Заголовок: {content['title']}")
        print(f"Длина контента: {len(content['content'])} символов")
        if image_url:
            print(f"Есть изображение")

    save_json(brands_data, 'brands.json')

    print("\n" + "=" * 50)
    print(f"Обработано брендов: {len(brands_data)}")
    print("=" * 50)

    return brands_data


if __name__ == '__main__':
    get_all_brands()