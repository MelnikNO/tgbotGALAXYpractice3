import subprocess
import sys
import time


def run_script(script_name, description):
    """Запускает скрипт и выводит информацию"""
    print("\n" + "=" * 60)
    print(f"{description}")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, script_name],
                                capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)
        return True
    except Exception as e:
        print(f"Ошибка при запуске {script_name}: {e}")
        return False


def main():
    print("\n" + "★" * 60)
    print("ПОЛНЫЙ ПАРСИНГ САЙТА mnogomoloka.ru")
    print("★" * 60)

    start_time = time.time()

    if not run_script('parse_text.py', 'ТЕКСТОВЫЕ СТРАНИЦЫ'):
        print("Остановлено из-за ошибки")
        return

    if not run_script('parse_brands.py', 'БРЕНДЫ'):
        print("Остановлено из-за ошибки")
        return

    if not run_script('parse_news.py', 'НОВОСТИ'):
        print("Остановлено из-за ошибки")
        return

    if not run_script('merge_data.py', 'ОБЪЕДИНЯЕМ ДАННЫЕ'):
        print("Остановлено из-за ошибки")
        return

    elapsed_time = time.time() - start_time
    print("\n" + "★" * 60)
    print(f"ПАРСИНГ ПОЛНОСТЬЮ ЗАВЕРШЕН за {elapsed_time:.1f} секунд!")
    print("Файл bot_data.json готов для использования в Telegram-боте")
    print("★" * 60)


if __name__ == '__main__':
    main()