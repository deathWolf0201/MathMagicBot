from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_dp import bot

router = Router()


class Magic1(StatesGroup):
    deactivate = State()
    first_num = State()
    reverse_first_num = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в магию чисел. Выберите один из 3-х фокусов в магической шляпе",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='1.Угадаю задуманное число', callback_data="magic1")],
                             [InlineKeyboardButton(text='2.', callback_data="magic2")],
                             [InlineKeyboardButton(text='3.', callback_data="magic3")]]))


@router.callback_query(F.data == "magic1")
async def magic1(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await remove_inline_keyboard(callback.from_user.id, callback.message.message_id)
    await state.set_state(Magic1.first_num)
    await callback.message.answer(
        "Напиши трехзначное число, в котором крайние цифры различны и отличаются друг от друга более чем на единицу.")


@router.message(Magic1.first_num)
async def magic1_first_num(message: Message, state: FSMContext):
    if message.text.isdigit():
        res = int(message.text)
        if 100 <= res <= 999:
            if abs(res // 100 - res % 10) > 1:
                await state.set_state(Magic1.reverse_first_num)
                await message.answer(
                    "Поменяй местами крайние цифры и вычти из большего трехзначного числа меньшее. Напиши, что у тебя получилось.")
                return
            await message.answer(
                "Данное число не соответствует условию. Нужно, чтобы разница между первой и последней цифрой была больше одного.")
            return
        await message.answer("Это не трёхзначное число")
        return
    await wrong_message(message)


@router.message(Magic1.reverse_first_num)
async def magic1_reverse_first_num(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.set_state(Magic1.deactivate)
        await message.answer(
            "Опять переставь крайние числа, и получившееся число прибавь к разности первых двух. Дай-ка угадаю, у тебя должно получиться число 1089!! Напиши, что у тебя получилось.")
        return
    await wrong_message(message)


@router.message(Magic1.deactivate)
async def magic1_deactivate(message: Message, state: FSMContext):
    if message.text.isdigit():
        match int(message.text):
            case 1089:
                await state.clear()
                await message.answer("Вот видишь, какой я хороший фокусник, да и ты справился с заданием на отлично!")
            case _:
                await message.answer("Проверь предыдущие шаги, возможно, ты где-то допустил ошибку…")
                return
        await message.answer("Спасибо, можешь выбрать другой фокус из волшебной шляпы!",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='1.Угадаю задуманное число', callback_data="magic1")],
                                 [InlineKeyboardButton(text='2.', callback_data="magic2")],
                                 [InlineKeyboardButton(text='3.', callback_data="magic3")]]))
        return
    await wrong_message(message)


@router.message()
async def wrong_message(message: Message):
    await message.answer("Неизвестная команда")


async def remove_inline_keyboard(chat_id, message_id):
    try:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        return
