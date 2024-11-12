from aiogram.filters import Filter
from aiogram import types


# Наследуемся от базового класса Filter.
class ChatTypeFilter(Filter):

    # Буем передавать список типов чатов в которых
    # будет работать тот или иной роутер.
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    # Чтобы фильтр сработал нужно переопределить этот метод - асинхронный.
    # Aiogram сам перекинет объект message -
    # сообщение, которое пользователь отправил.
    # PS: Так как сюда пробрасывается message - можно устроить любую проверку!
    async def __call__(self, message: types.Message) -> bool:
        # Тут проверяем что тип message имеется в списке наших типов
        return message.chat.type in self.chat_types
