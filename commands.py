import logging
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from constants import BUTTON_MENU, BACK_BUTTON, SECTION_ABOUT, SECTION_PRODUCTION, SECTION_BRANDS, SECTION_PRESS, SECTION_PARTNERS, SECTION_CONTACTS, DATA_FILE, WELCOME_MESSAGE, MENU_MASSAGE, ERROR_NOT_FOUND, STATE_NEWS, STATE_BRAND, STATE_SUBSECTION, STATE_SECTION, STATE_MAIN_MENU
import keyboards
from utils.helpers import load_data, get_brand_data, get_section_data, get_page_data, get_news, is_404_page
from templates import format_content, format_error_404, debug_page_data
logger = logging.getLogger(__name__)

DATA = {}
user_navigation = {}

def load_data_on_startup():
    """Загружает данные при запуске бота """
    global DATA
    DATA = load_data(DATA_FILE)
    if DATA:
        logger.info("Данные успешно загружены")
    else:
        logger.error("Ошибка загрузки данных")
        DATA = {}


def reset_search_context(context: CallbackContext) -> None:
    """ Сброс контекста поиска """
    keys_to_remove = ['current_section', 'current_page', 'search_results']
    for key in keys_to_remove:
        if key in context.user_data:
            del context.user_data[key]


async def start(update: Update, context: CallbackContext) -> None:
    """ Обработка команды /start """
    reset_search_context(context)
    user = update.effective_user
    chat_id = update.effective_chat.id

    if chat_id in user_navigation:
        del user_navigation[chat_id]

    logger.info(f"Пользователь {user.first_name} запустил бота")

    welcome_text = f"Здравствуйте, {user.first_name}!\n" + WELCOME_MESSAGE.format(
        phone=DATA.get('site_info', {}).get('phone', '8 800 555 90 14')
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown'
    )

    await update.message.reply_text(
        "Выберите раздел:",
        reply_markup=keyboards.main_menu_keyboard()
    )


async def show_menu(update: Update, context: CallbackContext) -> None:
    """ Показ главного меню """
    reset_search_context(context)

    if update.message:
        await update.message.reply_text(
            MENU_MASSAGE,
            reply_markup=keyboards.main_menu_keyboard()
        )
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            MENU_MASSAGE,
            reply_markup=keyboards.main_menu_keyboard_inline()
        )


async def handle_main_menu(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора в главном меню """
    text = update.message.text
    logger.info(f"Выбран раздел: {text}")

    logger.info(f"waiting_for_news_number: {context.user_data.get('waiting_for_news_number')}")
    logger.info(f"news_list length: {len(context.user_data.get('news_list', []))}")

    if context.user_data.get('waiting_for_news_number'):
        logger.info("Обработка номера новости")

        if text == BUTTON_MENU:
            context.user_data['waiting_for_news_number'] = False
            if 'news_list' in context.user_data:
                del context.user_data['news_list']
            await show_menu(update, context)
            return STATE_MAIN_MENU

        elif text == BACK_BUTTON:
            context.user_data['waiting_for_news_number'] = False
            if 'news_list' in context.user_data:
                del context.user_data['news_list']
            await show_press_section(update, context)
            return STATE_SECTION

        else:
            return await handle_news_number(update, context)

    if text == SECTION_ABOUT:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_company_section(update, context)
        return STATE_SECTION

    elif text == SECTION_PRODUCTION:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_production_section(update, context)
        return STATE_SECTION

    elif text == SECTION_BRANDS:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_brands_section(update, context)
        return STATE_SECTION

    elif text == SECTION_PRESS:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_press_section(update, context)
        return STATE_SECTION

    elif text == SECTION_PARTNERS:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_partners_section(update, context)
        return STATE_SECTION

    elif text == SECTION_CONTACTS:
        context.user_data['previous_state'] = STATE_MAIN_MENU
        await show_contacts_section(update, context)
        return STATE_SECTION

    elif text == BACK_BUTTON:
        await handle_back_button(update, context)
        return context.user_data.get('previous_state', STATE_MAIN_MENU)

    elif text == BUTTON_MENU:
        await show_menu(update, context)
        return STATE_MAIN_MENU

    else:
        await update.message.reply_text(
            "Пожалуйста, выберите пункт из меню.",
            reply_markup=keyboards.main_menu_keyboard()
        )
        return STATE_MAIN_MENU


async def show_company_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'О компании' """
    section = get_section_data(DATA, SECTION_ABOUT)

    if not section:
        await update.message.reply_text(ERROR_NOT_FOUND)
        return

    main_page = section.get('main_page', {})
    formatted_text = format_content('page', {
        'title': main_page.get('title', SECTION_ABOUT),
        'content': main_page.get('content', ''),
        'url': main_page.get('url')
    })

    await update.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Выберите подраздел:",
        reply_markup=keyboards.company_keyboard_inline()
    )


async def show_company_subsection(query, context: CallbackContext, subsection_key: str) -> None:
    """ Показывает подраздел из раздела 'О компании' """

    subsection_map = {
        "history": "История",
        "mission": "Миссия и ценности",
        "csr": "КСО",
        "health": "Здоровый образ жизни",
        "ecology": "Забота об окружающей среде",
        "space": "Сотрудничество с Роскосмос"
    }

    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_ABOUT

    subsection_name = subsection_map.get(subsection_key)
    if not subsection_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return

    page_data = get_page_data(DATA, SECTION_ABOUT, subsection_name)
    debug_page_data(page_data, subsection_name)

    if not page_data or is_404_page(page_data):
        await query.edit_message_text(
            format_error_404(subsection_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    formatted_text = format_content('page', {
        'title': page_data.get('title', subsection_name),
        'content': page_data.get('content', ''),
        'url': page_data.get('url')
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие подразделы:",
        reply_markup=keyboards.get_company_subsections_keyboard_inline(subsection_key)
    )
    return STATE_SUBSECTION


async def show_production_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'Производство' """
    section = get_section_data(DATA, SECTION_PRODUCTION)

    if not section:
        await update.message.reply_text(ERROR_NOT_FOUND)
        return

    main_page = section.get('main_page', {})
    formatted_text = format_content('page', {
        'title': main_page.get('title', SECTION_PRODUCTION),
        'content': main_page.get('content', ''),
        'url': main_page.get('url')
    })


    await update.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Выберите подраздел:",
        reply_markup=keyboards.production_keyboard_inline()
    )


async def show_production_subsection(query, context: CallbackContext, subsection_key: str) -> None:
    """ Показывает подраздел из раздела 'Производство' """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_PRODUCTION

    subsection_map = {
        "way": "Путь молока от фермы до потребителя",
        "technology": "Технологии",
        "guality": "Качество и безопасность"
    }

    subsection_name = subsection_map.get(subsection_key)
    if not subsection_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return STATE_SECTION

    page_data = get_page_data(DATA, SECTION_PRODUCTION, subsection_name)
    debug_page_data(page_data, subsection_name)

    if not page_data or is_404_page(page_data):
        await query.edit_message_text(
            format_error_404(subsection_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return STATE_SECTION

    formatted_text = format_content('page', {
        'title': page_data.get('title', subsection_name),
        'content': page_data.get('content', ''),
        'url': page_data.get('url')
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие подразделы:",
        reply_markup=keyboards.get_production_subsections_keyboard_inline(subsection_key)
    )

    return STATE_SUBSECTION


async def show_brands_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'Бренды' """
    message = f"*{SECTION_BRANDS}*\n\nВыберите бренд для просмотра информации:"

    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Наши бренды:",
        reply_markup=keyboards.brands_keyboards_inline()
    )


async def show_brand_info(query, context: CallbackContext, brand_key: str) -> None:
    """ Показывает информацию о бренде """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_BRANDS

    brand_map = {
        "svezhee": "Свежее Завтра",
        "DOBRYATA": "Добрята",
        "BIG_MUG": "Большая Кружка",
        "SUDARYNYA": "Сударыня",
        "TELUSHKA": "Тёлушка"
    }

    brand_name = brand_map.get(brand_key)
    if not brand_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return STATE_SECTION

    brand_data = get_brand_data(DATA, brand_name)

    if not brand_data or brand_data.get('title') == 'Ошибка 404':
        await query.edit_message_text(
            format_error_404(brand_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    formatted_text = format_content('brand', brand_data)

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие бренды:",
        reply_markup=keyboards.get_brands_keyboard_inline(brand_key)
    )
    return STATE_BRAND


async def show_press_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'Пресс-центр' """
    message = f"*{SECTION_PRESS}*\n\nВыберите раздел:"

    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Разделы пресс-центра:",
        reply_markup=keyboards.press_keyboards_inline()
    )


async def show_press_subsection(query, context: CallbackContext, subsection_key: str) -> None:
    """ Показывает подраздел из раздела 'Пресс-центр' """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_PRESS

    subsection_map = {
        "NEWS": "Новости",
        "GALLERY": "Галерея",
        "VIDEO": "Видео"
    }

    subsection_name = subsection_map.get(subsection_key)
    if not subsection_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return STATE_SECTION

    if subsection_key == "NEWS":
        await show_news_list(query, context)

    page_data = get_page_data(DATA, SECTION_PRESS, subsection_name)
    debug_page_data(page_data, subsection_name)

    if not page_data or is_404_page(page_data):
        await query.edit_message_text(
            format_error_404(subsection_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return STATE_SECTION

    formatted_text = format_content('page', {
        'title': page_data.get('title', subsection_name),
        'content': page_data.get('content', ''),
        'url': page_data.get('url')
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие подразделы:",
        reply_markup=keyboards.get_press_subsections_keyboard_inline(subsection_key)
    )

    return STATE_SUBSECTION


async def show_news_list(query, context: CallbackContext) -> None:
    """ Показывает список новостей """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_PRESS

    news_list = get_news(DATA, limit=10)

    if not news_list:
        await query.edit_message_text(
            "Новости пока отсутствуют",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return STATE_SECTION

    context.user_data['news_list'] = news_list
    context.user_data['waiting_for_news_number'] = True
    logger.info(f"Установлен waiting_for_news_number=True, новостей: {len(news_list)}")

    formatted_text = format_content('news_list', {
        'list': news_list,
        'page': 0
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    return STATE_NEWS


async def show_partners_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'Партнерам' """
    message = f"*{SECTION_PARTNERS}*\n\nВыберите категорию:"

    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Категории:",
        reply_markup=keyboards.partners_keyboards_inliine()
    )


async def show_partners_subsection(query, context: CallbackContext, subsection_key: str) -> None:
    """ Показывает подраздел из раздела 'Партнерам' """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_PARTNERS

    subsection_map = {
        "CLIENTS": "Клиентам",
        "PROVIDERS": "Поставщикам"
    }

    subsection_name = subsection_map.get(subsection_key)
    if not subsection_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return STATE_SECTION

    page_data = get_page_data(DATA, SECTION_PARTNERS, subsection_name)
    debug_page_data(page_data, subsection_name)

    if not page_data or is_404_page(page_data):
        await query.edit_message_text(
            format_error_404(subsection_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return STATE_SECTION

    formatted_text = format_content('page', {
        'title': page_data.get('title', subsection_name),
        'content': page_data.get('content', ''),
        'url': page_data.get('url')
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие подразделы:",
        reply_markup=keyboards.get_partners_subsections_keyboard_inline(subsection_key)
    )

    return STATE_SUBSECTION


async def show_contacts_section(update: Update, context: CallbackContext) -> None:
    """ Показывает раздел 'Контакты' """
    section = get_section_data(DATA, SECTION_CONTACTS)

    if not section:
        await update.message.reply_text(ERROR_NOT_FOUND)
        return

    main_page = section.get('main_page', {})

    formatted_text = format_content('contacts', {
        'content': main_page.get('content', ''),
        'url': main_page.get('url')
    })

    await update.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await update.message.reply_text(
        "Разделы контактов:",
        reply_markup=keyboards.contacts_keyboard_inline()
    )


async def show_contacts_subsection(query, context: CallbackContext, subsection_key: str) -> None:
    """ Показывает подраздел из раздела 'Контакты' """
    context.user_data['previous_state'] = STATE_SECTION
    context.user_data['current_section'] = SECTION_CONTACTS

    subsection_map = {
        "CONSUMERS": "Потребителям",
        "OFFICES": "Наши офисы",
        "JOURNALISTS": "Журналистам",
        "FAQ": "Вопрос-ответ",
        "JOBS": "Работа у нас"
    }

    subsection_name = subsection_map.get(subsection_key)
    if not subsection_name:
        await query.message.reply_text(ERROR_NOT_FOUND)
        return STATE_SECTION

    page_data = get_page_data(DATA, SECTION_CONTACTS, subsection_name)
    debug_page_data(page_data, subsection_name)

    if not page_data or is_404_page(page_data):
        await query.message.reply_text(
            format_error_404(subsection_name),
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return STATE_SECTION

    formatted_text = format_content('page', {
        'title': page_data.get('title', subsection_name),
        'content': page_data.get('content', ''),
        'url': page_data.get('url')
    })

    await query.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    await query.message.reply_text(
        "Другие подразделы:",
        reply_markup=keyboards.get_contacts_subsections_keyboard_inline(subsection_key)
    )

    return STATE_SUBSECTION


async def handle_callback(update: Update, context: CallbackContext) -> None:
    """ Главный обработчик всех callback-запросов """
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    logger.info(f"Callback: {callback_data}")

    if callback_data.startswith("company_"):
        subsection_key = callback_data.replace("company_", "")
        await show_company_subsection(query, context, subsection_key)

    elif callback_data.startswith("production_"):
        subsection_key = callback_data.replace("production_", "")
        await show_production_subsection(query, context, subsection_key)

    elif callback_data.startswith("brand_"):
        brand_key = callback_data.replace("brand_", "")
        await show_brand_info(query, context, brand_key)

    elif callback_data.startswith("press_"):
        subsection_key = callback_data.replace("press_", "")
        await show_press_subsection(query, context, subsection_key)

    elif callback_data.startswith("partners_"):
        subsection_key = callback_data.replace("partners_", "")
        await show_partners_subsection(query, context, subsection_key)

    elif callback_data.startswith("contacts_"):
        subsection_key = callback_data.replace("contacts_", "")
        await show_contacts_subsection(query, context, subsection_key)

    elif callback_data == "contacts":
        await show_contacts_section(update, context)

    elif callback_data == "web-site":
        await query.message.reply_text(
            "🌐 Наш сайт: https://mnogomoloka.ru"
        )

    elif callback_data in ["history", "mission", "csr", "health", "ecology", "space"]:
        await show_company_subsection(query, context, callback_data)

    elif callback_data in ["way", "technology", "guality"]:
        await show_production_subsection(query, context, callback_data)

    elif callback_data in ["svezhee", "DOBRYATA", "BIG_MUG", "SUDARYNYA", "TELUSHKA"]:
        await show_brand_info(query, context, callback_data)

    elif callback_data in ["CONSUMERS", "OFFICES", "JOURNALISTS", "FAQ", "JOBS"]:
        await show_contacts_subsection(query, context, callback_data)

    elif callback_data in ["CLIENTS", "PROVIDERS"]:
        await show_partners_subsection(query, context, callback_data)

    elif callback_data in ["GALLERY", "VIDEO"]:
        await show_press_subsection(query, context, callback_data)
    elif callback_data == "NEWS":
        logger.info("Выбраны новости")
        result = await show_news_list(query, context)
        return result

    else:
        await query.message.reply_text(ERROR_NOT_FOUND)


async def handle_text_message(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает все текстовые сообщения """
    text = update.message.text.strip()

    if context.user_data.get('waiting_for_news_number'):
        try:
            news_index = int(text) - 1
            news_list = context.user_data.get('news_list', [])

            if 0 <= news_index < len(news_list):
                news = news_list[news_index]
                formatted_news = format_content('news', news)

                await update.message.reply_text(
                    formatted_news,
                    parse_mode='Markdown',
                    reply_markup=keyboards.create_back_menu_keyboard()
                )

                context.user_data['waiting_for_news_number'] = False
                await show_news_list_from_message(update, context)
            else:
                await update.message.reply_text(
                    f"Введите число от 1 до {len(news_list)}",
                    reply_markup=keyboards.create_back_menu_keyboard()
                )
        except ValueError:
            await update.message.reply_text(
                "Пожалуйста, введите число",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите пункт из меню:",
            reply_markup=keyboards.main_menu_keyboard()
        )


async def show_news_list_from_message(update: Update, context: CallbackContext) -> None:
    """ Показывает список новостей (из сообщения) """
    news_list = get_news(DATA, limit=10)

    if not news_list:
        await update.message.reply_text(
            "Новости пока отсутствуют",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    context.user_data['news_list'] = news_list
    context.user_data['waiting_for_news_number'] = True

    formatted_text = format_content('news_list', {
        'list': news_list,
        'page': 0
    })

    await update.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )


def register_handlers(dp):
    """ Регистрирует все обработчики в диспетчере """
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STATE_MAIN_MENU: [
                MessageHandler(filters.text & ~filters.command, handle_main_menu)
            ],
            STATE_SECTION: [
                MessageHandler(filters.text & ~filters.command, handle_main_menu),
                CallbackQueryHandler(handle_callback)
            ],
            STATE_SUBSECTION: [
                MessageHandler(filters.text & ~filters.command, handle_main_menu),
                CallbackQueryHandler(handle_callback)
            ],
            STATE_BRAND: [
                MessageHandler(filters.text & ~filters.command, handle_main_menu),
                CallbackQueryHandler(handle_callback)
            ],
            STATE_NEWS: [
                MessageHandler(filters.text & ~filters.command, handle_main_menu),
                CallbackQueryHandler(handle_callback)
            ],
        },
        fallbacks=[CommandHandler("start", start)]
    )

    dp.add_handler(conv_handler)


async def handle_back_button(update: Update, context: CallbackContext) -> int:
    """ Обработка кнопки 'Назад' """
    if context.user_data.get('waiting_for_news_number'):
        context.user_data['waiting_for_news_number'] = False
        if 'news_list' in context.user_data:
            del context.user_data['news_list']
        await show_press_section(update, context)
        return STATE_SECTION

    previous_state = context.user_data.get('previous_state', STATE_MAIN_MENU)
    logger.info(f"Возврат в состояние: {previous_state}")

    if previous_state == STATE_MAIN_MENU:
        await show_menu(update, context)
        return STATE_MAIN_MENU

    elif previous_state == STATE_SECTION:
        current_section = context.user_data.get('current_section')
        if current_section == SECTION_ABOUT:
            await show_company_section(update, context)
        elif current_section == SECTION_PRODUCTION:
            await show_production_section(update, context)
        elif current_section == SECTION_BRANDS:
            await show_brands_section(update, context)
        elif current_section == SECTION_PRESS:
            await show_press_section(update, context)
        elif current_section == SECTION_PARTNERS:
            await show_partners_section(update, context)
        elif current_section == SECTION_CONTACTS:
            await show_contacts_section(update, context)
        else:
            await show_menu(update, context)
        return STATE_SECTION

    elif previous_state == STATE_SUBSECTION:
        current_section = context.user_data.get('current_section')
        if current_section == SECTION_ABOUT:
            await show_company_section(update, context)
        elif current_section == SECTION_PRODUCTION:
            await show_production_section(update, context)
        elif current_section == SECTION_BRANDS:
            await show_brands_section(update, context)
        elif current_section == SECTION_PRESS:
            await show_press_section(update, context)
        elif current_section == SECTION_PARTNERS:
            await show_partners_section(update, context)
        elif current_section == SECTION_CONTACTS:
            await show_contacts_section(update, context)
        return STATE_SECTION

    else:
        await show_menu(update, context)
        return STATE_MAIN_MENU


async def handle_news_number(update: Update, context: CallbackContext) -> int:
    """ Обрабатывает ввод номера новости """
    text = update.message.text.strip()
    logger.info(f"Ввод номера новости: {text}")

    try:
        news_index = int(text) - 1
        news_list = context.user_data.get('news_list', [])

        if 0 <= news_index < len(news_list):
            news = news_list[news_index]
            formatted_news = format_content('news', news)

            await update.message.reply_text(
                formatted_news,
                parse_mode='Markdown',
                reply_markup=keyboards.create_back_menu_keyboard()
            )

            await show_news_list_after_news(update, context)

        else:
            await update.message.reply_text(
                f"Введите число от 1 до {len(news_list)}",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите число",
            reply_markup=keyboards.create_back_menu_keyboard()
        )

    return STATE_NEWS


async def show_news_list_after_news(update: Update, context: CallbackContext) -> None:
    """ Показывает список новостей после просмотра одной новости """
    news_list = context.user_data.get('news_list', [])

    if not news_list:
        news_list = get_news(DATA, limit=10)
        context.user_data['news_list'] = news_list

    formatted_text = format_content('news_list', {
        'list': news_list,
        'page': 0
    })

    await update.message.reply_text(
        formatted_text,
        parse_mode='Markdown',
        reply_markup=keyboards.create_back_menu_keyboard()
    )