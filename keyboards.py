# Клавиатуры и кнопки

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from constants import BUTTON_MENU, BACK_BUTTON, SECTION_ABOUT, SECTION_PRODUCTION, SECTION_BRANDS, SECTION_PRESS, SECTION_PARTNERS, SECTION_CONTACTS, BUTTON_CONTACTS, BUTTON_WEBSITE, SUBSECTION_HISTORY, SUBSECTION_MISSION, SUBSECTION_CSR, SUBSECTION_HEALTH, SUBSECTION_ECOLOGY, SUBSECTION_SPACE, SUBSECTION_WAY, SUBSECTION_QUALITY, SUBSECTION_TECHNOLOGY, BRAND_SVEZHEE, BRAND_DOBRYATA, BRAND_BIG_MUG, BRAND_SUDARYNYA, BRAND_TELUSHKA, SUBSECTION_CONSUMERS, SUBSECTION_OFFICES, SUBSECTION_JOURNALISTS, SUBSECTION_FAQ, SUBSECTION_JOBS, SUBSECTION_CLIENTS, SUBSECTION_PROVIDERS, SUBSECTION_NEWS, SUBSECTION_GALLERY, SUBSECTION_VIDEO

def exit_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру с выходом в главное меню """
    keyboard = [[BUTTON_MENU]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def create_back_menu_keyboard() -> ReplyKeyboardMarkup:
    """ Универсальная клавиатура с кнопками 'Назад' и 'Меню' """
    keyboard = [
        [BACK_BUTTON],
        [BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """ Главное меню """
    keyboard = [
        [SECTION_ABOUT, SECTION_PRODUCTION],
        [SECTION_BRANDS, SECTION_PRESS],
        [SECTION_PARTNERS, SECTION_CONTACTS],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def main_menu_keyboard_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для главного меню """
    inline_keyboard = [[InlineKeyboardButton(BUTTON_CONTACTS, callback_data="contacts")],
                       [InlineKeyboardButton(BUTTON_WEBSITE, callback_data="web-site")]
                       ]
    return InlineKeyboardMarkup(inline_keyboard)


def company_keyboard_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "О компании" """
    inline_keyboard = [[InlineKeyboardButton(SUBSECTION_HISTORY, callback_data="history")],
                       [InlineKeyboardButton(SUBSECTION_MISSION, callback_data="mission")],
                       [InlineKeyboardButton(SUBSECTION_CSR, callback_data="csr")],
                       [InlineKeyboardButton(SUBSECTION_HEALTH, callback_data="health")],
                       [InlineKeyboardButton(SUBSECTION_ECOLOGY, callback_data="ecology")],
                       [InlineKeyboardButton(SUBSECTION_SPACE, callback_data="space")]
                       ]
    return InlineKeyboardMarkup(inline_keyboard)


def production_keyboard_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "Производство" """
    inline_keyboard = [
        [InlineKeyboardButton(SUBSECTION_WAY, callback_data="way")],
        [InlineKeyboardButton(SUBSECTION_TECHNOLOGY, callback_data="technology")],
        [InlineKeyboardButton(SUBSECTION_QUALITY, callback_data="guality")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def brands_keyboards_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "Бренды" """
    inline_keyboards = [
        [InlineKeyboardButton(BRAND_SVEZHEE, callback_data="svezhee")],
        [InlineKeyboardButton(BRAND_DOBRYATA, callback_data="DOBRYATA")],
        [InlineKeyboardButton(BRAND_BIG_MUG, callback_data="BIG_MUG")],
        [InlineKeyboardButton(BRAND_SUDARYNYA, callback_data="SUDARYNYA")],
        [InlineKeyboardButton(BRAND_TELUSHKA, callback_data="TELUSHKA")]
    ]
    return InlineKeyboardMarkup(inline_keyboards)


def contacts_keyboard_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "Контакты" """
    inline_keyboards = [
        [InlineKeyboardButton(SUBSECTION_CONSUMERS, callback_data="CONSUMERS")],
        [InlineKeyboardButton(SUBSECTION_OFFICES, callback_data="OFFICES")],
        [InlineKeyboardButton(SUBSECTION_JOURNALISTS, callback_data="JOURNALISTS")],
        [InlineKeyboardButton(SUBSECTION_FAQ, callback_data="FAQ")],
        [InlineKeyboardButton(SUBSECTION_JOBS, callback_data="JOBS")]
    ]
    return InlineKeyboardMarkup(inline_keyboards)


def partners_keyboards_inliine() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "Партнерам" """
    inline_keyboards = [
        [InlineKeyboardButton(SUBSECTION_CLIENTS, callback_data="CLIENTS")],
        [InlineKeyboardButton(SUBSECTION_PROVIDERS, callback_data="PROVIDERS")]
    ]
    return InlineKeyboardMarkup(inline_keyboards)


def press_keyboards_inline() -> InlineKeyboardMarkup:
    """ Инлайн-клавиатура для раздела "Пресс-центр" """
    inline_keyboards = [
        [InlineKeyboardButton(SUBSECTION_NEWS, callback_data="NEWS")],
        [InlineKeyboardButton(SUBSECTION_GALLERY, callback_data="GALLERY")],
        [InlineKeyboardButton(SUBSECTION_VIDEO, callback_data="VIDEO")]
    ]
    return InlineKeyboardMarkup(inline_keyboards)


def get_company_subsections_keyboard_inline(current_subsection: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с подразделами 'О компании' (кроме текущего) """

    all_subsections = [
        ("history", "История"),
        ("mission", "Миссия и ценности"),
        ("csr", "КСО"),
        ("health", "Здоровый образ жизни"),
        ("ecology", "Забота об окружающей среде"),
        ("space", "Сотрудничество с Роскосмос")
    ]

    keyboard = []
    row = []

    for key, name in all_subsections:
        if key == current_subsection:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"company_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_production_subsections_keyboard_inline(current_subsection: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с подразделами 'Производство' (кроме текущего) """

    all_subsections = [
        ("way", "Путь молока от фермы до потребителя"),
        ("technology", "Технологии"),
        ("guality", "Качество и безопасность")
    ]

    keyboard = []
    row = []

    for key, name in all_subsections:
        if key == current_subsection:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"production_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_brands_keyboard_inline(current_brand: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с брендами (кроме текущего) """

    all_brands = [
        ("svezhee", "Свежее Завтра"),
        ("DOBRYATA", "Добрята"),
        ("BIG_MUG", "Большая Кружка"),
        ("SUDARYNYA", "Сударыня"),
        ("TELUSHKA", "Тёлушка")
    ]

    keyboard = []
    row = []

    for key, name in all_brands:
        if key == current_brand:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"brand_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_press_subsections_keyboard_inline(current_subsection: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с подразделами 'Пресс-центр' (кроме текущего) """

    all_subsections = [
        ("NEWS", "Новости"),
        ("GALLERY", "Галерея"),
        ("VIDEO", "Видео")
    ]

    keyboard = []
    row = []

    for key, name in all_subsections:
        if key == current_subsection:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"press_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_partners_subsections_keyboard_inline(current_subsection: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с подразделами 'Партнерам' (кроме текущего) """

    all_subsections = [
        ("CLIENTS", "Клиентам"),
        ("PROVIDERS", "Поставщикам")
    ]

    keyboard = []
    row = []

    for key, name in all_subsections:
        if key == current_subsection:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"partners_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_contacts_subsections_keyboard_inline(current_subsection: str = None) -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру с подразделами 'Контакты' (кроме текущего) """

    all_subsections = [
        ("CONSUMERS", "Потребителям"),
        ("OFFICES", "Наши офисы"),
        ("JOURNALISTS", "Журналистам"),
        ("FAQ", "Вопрос-ответ"),
        ("JOBS", "Работа у нас")
    ]

    keyboard = []
    row = []

    for key, name in all_subsections:
        if key == current_subsection:
            continue

        row.append(InlineKeyboardButton(name, callback_data=f"contacts_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)