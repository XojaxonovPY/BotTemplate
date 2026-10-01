import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.handlers import dp
from core.env_data import BotConfig
from db.engine import engine


async def on_startup(bot: Bot) -> None:
    """Bot ishga tushganda bajariladigan amallar."""
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
    ]
    await bot.set_my_commands(commands=commands)
    logging.info("Bot buyruqlari muvaffaqiyatli o'rnatildi.")


async def main() -> None:
    bot = Bot(
        token=BotConfig.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp.startup.register(on_startup)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("The bot is starting up in polling mode...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()
        logging.info("The bot session has closed.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        stream=sys.stdout,
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("The bot has been stopped.")
