from bot.dispatcher import dp
from bot.handlers.main_handler import router

dp.include_router(router)
