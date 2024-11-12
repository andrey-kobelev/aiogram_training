from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class FormCallBack(CallbackData, prefix='form'):
    yes_or_no: int


def get_form_inline_keyboard():
    keyboard = InlineKeyboardBuilder()
    for text, data in (('Да', 1), ('Нет', 0)):
        keyboard.add(InlineKeyboardButton(
            text=text,
            callback_data=FormCallBack(yes_or_no=data).pack()
        ))
    return keyboard.adjust(2,).as_markup()


def get_inline_keyboard(
        # * - автоматический запрет на передачу неименованных аргументов.
        *,
        # В словаре будет указываться text как ключ,
        # а в value - строка с данными, которые отправятся боту.
        buttons: dict,
        sizes: tuple[int] = (2,)
):
    keyboard = InlineKeyboardBuilder()
    # Проходимся по словарю
    for text, data in buttons.items():
        # Reply-кнопки отправляют только то,
        # что на них написано прям в чат, а inline нет.
        # Параметр text - только для отображения,
        # а в callback_data передаются данные,
        # которые бот сможет как то обработать
        # хендлером отлавливающим CallbackQuery-события.
        # PS: callback_data не отправляется в чат,
        # то есть эти данные невидимы для пользователя.
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


# Если понадобятся кнопки с URL
def get_keyboard_with_url_buttons(
        *,
        buttons: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


# Создать микс из CallBack и URL кнопок
def get_inline_keyboard_with_mix_buttons(
        *,
        buttons: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()
