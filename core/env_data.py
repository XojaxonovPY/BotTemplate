from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from core.settings import Env_path

load_dotenv(Env_path)


class BotConfig:
    TOKEN = getenv('BOT_TOKEN')
    PAYMENT_CLICK_TOKEN = getenv('PAYMENT_CLICK_TOKEN')


class DBConfig:
    DB_URL = getenv('DB_URL')


class WebConfig:
    ADMIN_USERNAME = getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD')


class Config:
    bot = BotConfig()
    dp = DBConfig()
    web = WebConfig()


UZB_TZ = ZoneInfo("Asia/Tashkent")


def get_current_uzb_time() -> datetime:
    return datetime.now(UZB_TZ)
