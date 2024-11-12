from aiogram import types, Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from app.filters.filters import ChatTypeFilter
from app.keyboards import reply, inline


# Список разрешенных типов чатов.
CHAT_TYPES = [
    'private',
]

user_private_router = Router()

user_private_router.message.filter(
    ChatTypeFilter(CHAT_TYPES)
)

FORM_BUTTON = 'Заполнить анкету'
ABOUT_BUTTON = 'О нас'

START_KEYBOARD = reply.get_reply_keyboard(
    FORM_BUTTON, ABOUT_BUTTON,
    placeholder='бла бла бла'
)


# С помощью готовой системы фильтрации хендлер
# будет реагировать на /start нужным образом.
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):

    await message.answer(
        text=(
            f'Привет, {message.from_user.username}! '
            f'Я отвечаю на сообщение /start'
        ),
        # Вторым параметром можно передать клавиатуру.
        reply_markup=START_KEYBOARD
    )


@user_private_router.message(F.text == ABOUT_BUTTON)
async def about_cmd(message: types.Message):
    text = (
        'Лучшая команда! На этом о нас всё.'
    )
    # Если до этого была клавиатура, она так и останется,
    # пока не передать новую или не удалить.
    # Чтобы удалить клаву, понадобится такой аргумент:
    # reply_markup=ReplyKeyboardRemove()
    await message.answer(
        text=text
    )


# Start FSM

class FormStates(StatesGroup):
    # Каждый пункт это состояние на котором
    # может находиться каждый пользователь.
    smoking = State()
    married = State()


# 1) FSM начнется, если у пользователя
# нет активных состояний - StateFilter(None).
# Это точка входа в состояние.
@user_private_router.message(StateFilter(None), F.text == FORM_BUTTON)
async def start_form(message: types.Message, state: FSMContext):
    await message.answer(
        text='Вы курите?',
        reply_markup=inline.get_form_inline_keyboard()
    )
    # Нужно указать в какое состояние нужно стать
    await state.set_state(FormStates.smoking)


# 2) Если пользователь в состоянии FormStates.smoking
# и callback_data соответствуют FormCallBack,
# то продолжаем FSM
@user_private_router.callback_query(
    FormStates.smoking,
    inline.FormCallBack.filter()
)
async def add_smoking_data(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: inline.FormCallBack,
):
    # Записать данные из запроса (callback_data) в state
    await state.update_data(is_smoking=callback_data.yes_or_no)

    # Данная конструкция нужна для того,
    # что-бы по центру отобразился полупрозрачный
    # всплывающий текст 'Ответ принят. Едем дальше'.
    # Конструкция необходима, так как нужно
    # серверу дать сигнал о том, что мы приняли callback_query!
    # PS: Скобки можно оставить пустыми.
    await callback.answer('Ответ принят. Едем дальше')

    await callback.message.answer(
        text='Состоите в браке?',
        reply_markup=inline.get_form_inline_keyboard()
    )
    # Нужно поменять состояние на следующее по цепи
    await state.set_state(FormStates.married)


# 3) Если пользователь в состоянии FormStates.married
# и callback_data соответствуют FormCallBack,
# то продолжаем FSM - завершаем.
@user_private_router.callback_query(
    FormStates.married,
    inline.FormCallBack.filter()
)
async def add_married_data_and_finish_form(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: inline.FormCallBack,
):
    await state.update_data(is_married=callback_data.yes_or_no)

    # Подтягиваем все накопившееся данные из сервера сюда в код
    data = await state.get_data()

    await callback.answer('Ответ принят. Идите отдыхать')

    await callback.message.answer(
        text=f'Вот данные, которые мы собрали '
             f'в ходе заполнения анкеты: {data}. '
             f'А можно было бы и в БД сохранить..'
    )

    # Очищаем данные и убираем все состояния.
    await state.clear()
