import asyncio
import os

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.handlers import ROUTERS


dotenv.load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# Бот будет работать только с апдейтом типа message (сообщения).
# Так же есть и такие типы апдейтов:
#   - 'edited_message' - измененные сообщения
#   - 'callback_query' - про данный тип позже
ALLOWED_UPDATES = ['message', 'callback_query']

# Класс самого бота - инициализация.
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
bot.admins = []

# Обрабатывает все апдейты из сервера - всё что касается бота.
# Отвечает за фильтрацию сообщений полученных с сервера.
# PS:
# В предыдущей версии нужно было передать объект бота.
dispatcher = Dispatcher()
dispatcher.include_routers(*ROUTERS)


async def on_startup_func(bot: Bot):
    print('Запустили бот')


async def on_shutdown_func(bot: Bot):
    print('Завершили бот')


async def main():
    # При СТАРТЕ бота выполнится функция переданная
    # в качестве аргумента в виде ссылки.
    dispatcher.startup.register(on_startup_func)

    # При ЗАВЕРШЕНИИ бота выполнится функция переданная
    # в качестве аргумента в виде ссылки.
    dispatcher.shutdown.register(on_shutdown_func)

    # Перед запуском сбрасываем старые обновления и начнем пуллинг с новых.
    # Делается для того, чтобы бот не начал отвечать сразу
    # на все 1000 пропущенных сообщений.
    await bot.delete_webhook(drop_pending_updates=True)

    # Здесь бот начнет слушать сервер ТГ,
    # и спрашивать у него о наличии обновлений.
    await dispatcher.start_polling(
        bot,
        # Указываем какие апдейты будем обрабатывать.
        allowed_updates=ALLOWED_UPDATES,
        # Альтернативный вариант allowed_updates ниже
        # Что-бы не прописывать каждый тип апдейта.
        # Те апдейты, которые мы используем -
        # автоматически будут передаваться сюда.
        # allowed_updates=dispatcher.resolve_used_update_types()
    )


if __name__ == '__main__':
    asyncio.run(main())
