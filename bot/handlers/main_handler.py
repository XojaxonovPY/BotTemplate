from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup

from bot.buttons.reply import reply_button_builder
from db.models import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    user_data: dict = {
        'user_id': message.chat.id,
        'username': message.chat.username
    }
    await User.check_user(user_data)
    buttons: list[str] = ['👤 Current User', '👥 Users']
    markup: ReplyKeyboardMarkup = reply_button_builder(buttons, (2,))
    await message.answer(text='Welcome to bot', reply_markup=markup)


@router.message(F.text == '👤 Current User')
async def current_user_handler(message: Message):
    user_obj = await User.get(User.user_id == message.chat.id)
    await message.answer(text=f'Salom {user_obj.username}')


@router.message(F.text == '👥 Users')
async def current_user_handler(message: Message):
    user_obj = await User.get_all(fields=["username"])
    for user in user_obj:
        await message.answer(text=f'Salom {user.username}')
