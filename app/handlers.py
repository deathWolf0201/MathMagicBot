from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_dp import bot

router = Router()


class Magic1(StatesGroup):
    deactivate = State()
    first_num = State()
    reverse_first_num = State()


class Magic2(StatesGroup):
    date_input = State()
    high_2 = State()
    add_5 = State()
    high_50 = State()
    add_month = State()
    res_number = State()


class Magic3(StatesGroup):
    num_input = State()
    digit_sum = State()
    sub_sum = State()
    cross_digit = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в магию чисел. Выберите один из 3-х фокусов в магической шляпе",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='ПРЕДСКАЖУ РЕЗУЛЬТАТ ДЕЙСТВИЙ НАД ЗАДУМАННЫМ ЧИСЛОМ',
                                                   callback_data="magic1")],
                             [InlineKeyboardButton(text='УГАДАЮ ТВОЙ ДЕНЬ РОЖДЕНИЯ', callback_data="magic2")],
                             [InlineKeyboardButton(text='УГАДАЮ ЗАЧЕРКНУТУЮ ЦИФРУ', callback_data="magic3")]]))


@router.callback_query(F.data == "magic1")
async def magic1(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await remove_inline_keyboard(callback.from_user.id, callback.message.message_id)
    await state.set_state(Magic1.first_num)
    await callback.message.answer(
        "Загадай трехзначное число, в котором крайние цифры различны и отличаются друг от друга более чем на единицу.",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загадал')]], resize_keyboard=True,
                                         one_time_keyboard=True))


@router.callback_query(F.data == "magic2")
async def magic2(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await remove_inline_keyboard(callback.from_user.id, callback.message.message_id)
    await state.set_state(Magic2.date_input)
    await callback.message.answer(
        "Загадай любую дату рождения.",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загадал')]], resize_keyboard=True,
                                         one_time_keyboard=True))


@router.callback_query(F.data == "magic3")
async def magic3(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await remove_inline_keyboard(callback.from_user.id, callback.message.message_id)
    await state.set_state(Magic3.num_input)
    await callback.message.answer(
        "Загадай любое многозначное число.",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загадал')]], resize_keyboard=True,
                                         one_time_keyboard=True))


@router.message(Magic1.first_num)
async def magic1_first_num(message: Message, state: FSMContext):
    match message.text:
        case "Загадал":
            await state.set_state(Magic1.reverse_first_num)
            await message.answer(
                "Поменяй местами крайние цифры и вычти из большего трехзначного числа меньшее.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поменял')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic1.reverse_first_num)
async def magic1_reverse_first_num(message: Message, state: FSMContext):
    match message.text:
        case "Поменял":
            await state.set_state(Magic1.deactivate)
            await message.answer(
                "Опять переставь крайние числа, и получившееся число прибавь к разности первых двух. Дай-ка угадаю, "
                "у тебя должно получиться число 1089!! Верно?",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')], [KeyboardButton(text='Нет')]],
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic1.deactivate)
async def magic1_deactivate(message: Message, state: FSMContext):
    match message.text:
        case "Да":
            await message.answer("Вот видишь, какой я хороший фокусник, да и ты справился с заданием на отлично!")
        case "Нет":
            await message.answer("Проверь предыдущие шаги, возможно, ты где-то допустил ошибку…")
        case _:
            await wrong_message(message)
            return
    await state.clear()
    await change_trick(message)


@router.message(Magic2.date_input)
async def date_input(message: Message, state: FSMContext):
    match message.text:
        case "Загадал":
            await state.set_state(Magic2.high_2)
            await message.answer(
                "Умножь на 2 число дня рождения.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Умножил')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic2.high_2)
async def high_2(message: Message, state: FSMContext):
    match message.text:
        case "Умножил":
            await state.set_state(Magic2.add_5)
            await message.answer(
                "К результату прибавь 5.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Прибавил')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic2.add_5)
async def add_5(message: Message, state: FSMContext):
    match message.text:
        case "Прибавил":
            await state.set_state(Magic2.high_50)
            await message.answer(
                "Умножь результат на 50.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Умножил')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic2.high_50)
async def high_50(message: Message, state: FSMContext):
    match message.text:
        case "Умножил":
            await state.set_state(Magic2.add_month)
            await message.answer(
                "Прибавь номер месяца рождения.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Прибавил')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic2.add_month)
async def add_month(message: Message, state: FSMContext):
    match message.text:
        case "Прибавил":
            await state.set_state(Magic2.res_number)
            await message.answer("Введи полученное число.")
        case _:
            await wrong_message(message)


@router.message(Magic2.res_number)
async def res_number(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.clear()
        Magic2.res_number.res = int(message.text) - 250
        await message.answer(
            f"Ваш день и месяц рождения: {Magic2.res_number.res // 100}.{"%02d" % (Magic2.res_number.res % 100)}")
        await change_trick(message)
        return
    await message.answer("Я ожидаю получить число. Причём целое.")


@router.message(Magic3.num_input)
async def num_input(message: Message, state: FSMContext):
    match message.text:
        case "Загадал":
            await state.set_state(Magic3.digit_sum)
            await message.answer(
                "Найди сумму цифр этого числа.",
                reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нашёл')]], resize_keyboard=True,
                                                 one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic3.digit_sum)
async def digit_sum(message: Message, state: FSMContext):
    match message.text:
        case "Нашёл":
            await state.set_state(Magic3.sub_sum)
            await message.answer("Отними от задуманного числа эту сумму цифр.",
                                 reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отнял')]],
                                                                  resize_keyboard=True,
                                                                  one_time_keyboard=True))
        case _:
            await wrong_message(message)


@router.message(Magic3.sub_sum)
async def digit_sum(message: Message, state: FSMContext):
    match message.text:
        case "Отнял":
            await state.set_state(Magic3.cross_digit)
            await message.answer("В числе, которое получится, зачеркни любую цифру и введи остальные.")
        case _:
            await wrong_message(message)


@router.message(Magic3.cross_digit)
async def digit_sum(message: Message, state: FSMContext):
    if message.text.isdigit():
        num = int(message.text)
        summ = 0
        while num > 0:
            summ += num % 10
            num //= 10
        await message.answer(f"Зачёркнутая цифра: {(summ // 9 + 1) * 9 - summ}")
        await state.clear()
        await change_trick(message)
        return
    await message.answer("Я ожидаю получить число. Причём целое.")


@router.message()
async def wrong_message(message: Message):
    await message.answer("Неизвестная команда")


async def remove_inline_keyboard(chat_id, message_id):
    try:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        return


async def change_trick(message: Message):
    await message.answer("Спасибо, можешь выбрать другой фокус из волшебной шляпы!",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='ПРЕДСКАЖУ РЕЗУЛЬТАТ ДЕЙСТВИЙ НАД ЗАДУМАННЫМ ЧИСЛОМ',
                                                   callback_data="magic1")],
                             [InlineKeyboardButton(text='УГАДАЮ ТВОЙ ДЕНЬ РОЖДЕНИЯ', callback_data="magic2")],
                             [InlineKeyboardButton(text='УГАДАЮ ЗАЧЕРКНУТУЮ ЦИФРУ', callback_data="magic3")]]))
