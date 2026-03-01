# Константы и тексты сообщений
# Сообщения
WELCOME_MESSAGE = """
**Галактика**\n
__Крупный производитель молочных продуктов в России__\n
Добро пожаловать в бот компании «Галактика»!\n
Здесь вы можете узнать информацию о компании с официального сайта, не выходя из приложения.\n
Сайт: https://mnogomoloka.ru/\n
**Выберите интересующий вас раздел.**
"""

MENU_MASSAGE = (
    "Вы в главном меню.\n"
    "Выберите интересующий вас раздел."
)

NO_RESULTS_MESSAGE = ("Ничего не найдено.\n"
                      "Попробуйте изменить запрос.")

EXIT = (
    "Вы можете вернуться в главное меню и поменять вариант поиска."
)

ERROR_404 = "Страница временно недоступна"
ERROR_NOT_FOUND = "Раздел не найден"

# Название кнопки/фильтров/файлов
NOT_FOUND = "Не указано"
BUTTON_MENU = "Главное меню"
BACK_BUTTON = "Назад"

DATA_FILE = 'parsing/bot_data.json'

BUTTON_CONTACTS = "Контакты"
BUTTON_NEWS = "Новости"
BUTTON_WEBSITE = "Открыть на сайте"
# Названия разделов
SECTION_ABOUT = "О компании"
SECTION_PRODUCTION = "Производство"
SECTION_BRANDS = "Бренды"
SECTION_PRESS = "Пресс-центр"
SECTION_PARTNERS = "Партнерам"
SECTION_CONTACTS = "Контакты"
# О компании
SUBSECTION_HISTORY = "История"
SUBSECTION_MISSION = "Миссия и ценности"
SUBSECTION_CSR = "КСО"
SUBSECTION_HEALTH = "Здоровый образ жизни"
SUBSECTION_ECOLOGY = "Забота об окружающей среде"
SUBSECTION_SPACE = "Сотрудничество с Роскосмос"
# Производство
SUBSECTION_WAY = "Путь молока от фермы до потребителя"
SUBSECTION_TECHNOLOGY = "Технологии"
SUBSECTION_QUALITY = "Качество и безопасность"
# Пресс-центр
SUBSECTION_NEWS = "Новости"
SUBSECTION_GALLERY = "Галерея"
SUBSECTION_VIDEO = "Видео"
# Партнерам
SUBSECTION_CLIENTS = "Клиентам"
SUBSECTION_PROVIDERS = "Поставщикам"
# Контакты
SUBSECTION_CONSUMERS = "Потребителям"
SUBSECTION_OFFICES = "Наши офисы"
SUBSECTION_JOURNALISTS = "Журналистам"
SUBSECTION_FAQ = "Вопрос-ответ"
SUBSECTION_JOBS = "Работа у нас"
# Бренды
BRAND_SVEZHEE = "Свежее Завтра"
BRAND_BIG_MUG = "Большая Кружка"
BRAND_DOBRYATA = "Добрята"
BRAND_SUDARYNYA = "Сударыня"
BRAND_TELUSHKA = "Тёлушка"

# Состояния для навигации
STATE_MAIN_MENU = 0
STATE_SECTION = 1
STATE_SUBSECTION = 2
STATE_BRAND = 3
STATE_NEWS = 4