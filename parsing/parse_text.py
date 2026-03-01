from config import SITE_STRUCTURE, OTHER_PAGES
from utils import get_page, extract_text_content, save_json, make_full_url


def parse_all_text_pages():
    """Парсит все текстовые страницы, сохраняя структуру разделов"""

    result = {
        "sections": {},
        "other_pages": {}
    }

    print("=" * 50)
    print("НАЧИНАЕМ ПАРСИНГ ТЕКСТОВЫХ СТРАНИЦ")
    print("=" * 50)

    for section_name, section_data in SITE_STRUCTURE.items():
        print(f"\nРАЗДЕЛ: {section_name}")

        section_result = {
            "name": section_name,
            "url": make_full_url(section_data["url"]),
            "main_page": None,
            "subsections": {}
        }

        if section_data["url"]:
            soup = get_page(make_full_url(section_data["url"]))
            if soup:
                section_result["main_page"] = extract_text_content(soup, make_full_url(section_data["url"]))
                print(f"Главная страница раздела обработана")

        for sub_name, sub_path in section_data.get("subsections", {}).items():
            print(f"Подраздел: {sub_name}")
            sub_url = make_full_url(sub_path)
            soup = get_page(sub_url)
            if soup:
                section_result["subsections"][sub_name] = extract_text_content(soup, sub_url)
                print(f"Обработан")
            else:
                section_result["subsections"][sub_name] = {"error": "Не удалось загрузить"}

        result["sections"][section_name] = section_result

    print(f"\nОТДЕЛЬНЫЕ СТРАНИЦЫ")
    for page_name, page_path in OTHER_PAGES.items():
        print(f"{page_name}")
        page_url = make_full_url(page_path)
        soup = get_page(page_url)
        if soup:
            result["other_pages"][page_name] = extract_text_content(soup, page_url)
            print(f"Обработана")
        else:
            result["other_pages"][page_name] = {"error": "Не удалось загрузить"}

    save_json(result, 'text_pages.json')

    print("\n" + "=" * 50)
    print("СТАТИСТИКА:")
    sections_count = len(result["sections"])
    subsections_count = sum(len(s["subsections"]) for s in result["sections"].values())
    other_count = len(result["other_pages"])
    print(f"  Разделов: {sections_count}")
    print(f"  Подразделов: {subsections_count}")
    print(f"  Отдельных страниц: {other_count}")
    print(f"  ВСЕГО: {sections_count + subsections_count + other_count}")
    print("=" * 50)

    return result


if __name__ == '__main__':
    parse_all_text_pages()