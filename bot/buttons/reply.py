from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


async def reply_button_builder(text: list[str], size=(1,), one_time=False) -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=i) for i in text])
    rkb.adjust(*size)
    rkb = rkb.as_markup(resize_keyboard=True)
    print(type(rkb))
    return rkb
