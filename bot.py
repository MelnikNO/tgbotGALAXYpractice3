""" Главный файл запуска бота """
import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from commands import (
    load_data_on_startup,
    start,
    handle_main_menu,
    handle_callback,
    handle_text_message
)
from constants import DATA_FILE

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_deep_link(update, context):
    """
    Обработка глубоких ссылок вида /start параметр
    Используется для переходов из карточек лендинга
    """
    args = context.args

    if args:
        command = args[0]

        # Связь параметров из ссылок с текстом ответа
        sections = {
            'about': (
                '📰 **О компании**\n\n'
                'Группа компаний «Галактика» — крупный независимый производитель '
                'широкого спектра молочных продуктов.\n\n'
                '«Галактика» полностью реализует всю цепочку производства молочных продуктов '
                'от фермы и до полки в торговой точке, именно поэтому выпускаемые молочные '
                'продукты проходят максимально короткий путь от коровы до потребителя.'
            ),
            'production': (
                '🏭 **Производство**\n\n'
                'Основной целью ГК «Галактика» является сохранение неизменного качества '
                'продукции и репутации компании.\n\n'
                'Для производства всего спектра молочных продуктов используется только молоко '
                'высшего качества фермерских хозяйств, расположенных в Ленинградской и '
                'Кировской области.'
            ),
            'brands': (
                '🏷️ **Наши бренды**\n\n'
                'Основное направление в деятельности компании на сегодняшний день — это '
                'производство и продажа широкого ассортимента молочных продуктов под '
                'собственными брендами.'
            ),
            'press': (
                '📢 **Пресс-центр**\n\n'
                'Новости, публикации, анонсы для СМИ.\n\n'
                'По вопросам сотрудничества со СМИ обращайтесь:\n'
                '📧 press@galaktika.ru'
            ),
            'partners': (
                '🤝 **Партнерам**\n\n'
                'Компания «Галактика» заинтересована в благополучии своих партнеров и '
                'нацелена на долгосрочное сотрудничество с клиентами и поставщиками.\n\n'
                'Мы постоянно ищем новые идеи, улучшаем нашу работу, развиваем отношения с '
                'партнерами, чтобы мир вокруг нас становился ярче и совершеннее.'
            ),
            'contacts': (
                '📞 **Контакты**\n\n'
                '📍 Адрес: г. Москва, ул. Примерная, д. 123\n'
                '📱 Телефон: 8 800 555 90 14\n'
                '📧 Email: info@galaktika.ru\n'
                '🌐 Сайт: https://mnogomoloka.ru\n\n'
                '🕒 Режим работы: Пн-Пт с 9:00 до 18:00'
            ),
            'contacts_inline': (
                '📱 **Свяжитесь с нами**\n\n'
                '📞 Телефон: 8 800 555 90 14\n'
                '📧 Email: info@galaktika.ru\n'
                '💬 Telegram: @galaxy_milk_bot'
            )
        }

        if command in sections:
            await update.message.reply_text(
                sections[command],
                parse_mode='Markdown'
            )
            logger.info(f"Пользователь {update.effective_user.id} запросил раздел: {command}")
            return

    # Если команда без параметра или параметр не найден — обычное приветствие
    await start(update, context)


async def main():
    """ Главная функция запуска бота """
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("Токен не найден")
        return

    logger.info("Токен загружен")

    logger.info(f"Загрузка данных из {DATA_FILE}...")
    load_data_on_startup()

    application = Application.builder().token(token).build()
    logger.info("Application создан")

    application.add_handler(CommandHandler("start", handle_deep_link))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_main_menu
    ))

    application.add_handler(CallbackQueryHandler(handle_callback))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_message
    ))

    logger.info("Все обработчики зарегистрированы")

    logger.info("Бот запускается...")

    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        logger.info("Бот успешно запущен и работает!")

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        logger.info("Бот остановлен")


if __name__ == '__main__':
    asyncio.run(main())