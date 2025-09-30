from aiogram import Bot, Dispatcher
from config.bot import BOT_TOKEN

# РОМА ДОПИШИ
from .routers.user import user_router                   # pyright: ignore
from .routers.base import base_router, prompts_router   # pyright: ignore
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(base_router)
dp.include_router(user_router)
dp.include_router(prompts_router)

__all__ = ["bot", "dp"]