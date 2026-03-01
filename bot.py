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

    application.add_handler(CommandHandler("start", start))

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