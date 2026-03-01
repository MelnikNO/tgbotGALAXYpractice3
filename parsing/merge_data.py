import json
import time


def merge_all_data():
    """Объединяет все спарсенные данные в один файл"""

    print("=" * 50)
    print("ОБЪЕДИНЕНИЕ ДАННЫХ")
    print("=" * 50)

    final_data = {
        'site_info': {
            'name': 'МногоМолока',
            'url': 'https://mnogomoloka.ru',
            'phone': '8 800 555 90 14',
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        },
        'structure': {},
        'brands': [],
        'news': []
    }

    try:
        with open('text_pages.json', 'r', encoding='utf-8') as f:
            text_data = json.load(f)
            final_data['structure'] = text_data
        print("Загружены текстовые страницы")

        sections_count = len(text_data.get('sections', {}))
        subsections_count = sum(len(s.get('subsections', {})) for s in text_data.get('sections', {}).values())
        other_count = len(text_data.get('other_pages', {}))
        print(f"- Разделов: {sections_count}")
        print(f"- Подразделов: {subsections_count}")
        print(f"- Отдельных страниц: {other_count}")

    except FileNotFoundError:
        print("text_pages.json не найден")
        final_data['structure'] = {'sections': {}, 'other_pages': {}}

    try:
        with open('brands.json', 'r', encoding='utf-8') as f:
            final_data['brands'] = json.load(f)
        print(f"Загружены бренды: {len(final_data['brands'])} шт.")
    except FileNotFoundError:
        print("⚠brands.json не найден")
        final_data['brands'] = []

    try:
        with open('news.json', 'r', encoding='utf-8') as f:
            final_data['news'] = json.load(f)
        print(f"Загружены новости: {len(final_data['news'])} шт.")
    except FileNotFoundError:
        print("news.json не найден")
        final_data['news'] = []

    output_file = 'bot_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print(f"ГОТОВО! Данные для бота сохранены в {output_file}")
    print("=" * 50)

    print("\nИТОГОВАЯ СТАТИСТИКА:")
    print(f"Текстовых страниц всего: {sections_count + subsections_count + other_count}")
    print(f"Брендов: {len(final_data['brands'])}")
    print(f"Новостей: {len(final_data['news'])}")
    print(f"ВСЕГО страниц: {sections_count + subsections_count + other_count + len(final_data['brands']) + len(final_data['news'])}")


if __name__ == '__main__':
    merge_all_data()