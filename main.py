import logging
import asyncio
import sys
from aiogram.dispatcher.event.bases import CancelHandler

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, BaseMiddleware, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from config import settings
from app.handlers import router, blocked_users


class BlockCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Update, data: dict):
        """Middleware для проверки заблокированных пользователей."""
        user_id = None
        username = None

        if hasattr(event, "message") and event.message:
            user_id = event.message.from_user.id
            username = event.message.from_user.username
        elif hasattr(event, "callback_query") and event.callback_query:
            user_id = event.callback_query.from_user.id
            username = event.callback_query.from_user.username
        elif hasattr(event, "inline_query") and event.inline_query:
            user_id = event.inline_query.from_user.id
            username = event.inline_query.from_user.username

        if user_id and (str(user_id) in blocked_users or (username and username in blocked_users)):
            if hasattr(event, "message") and event.message:
                await event.message.answer("Вы заблокированы и не можете использовать этого бота.")
            elif hasattr(event, "callback_query") and event.callback_query:
                await event.callback_query.answer("Вы заблокированы.", show_alert=True)
            raise CancelHandler()

        return await handler(event, data)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # dp = Dispatcher(storage=RedisStorage.from_url("redis://localhost:6379"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(BlockCheckMiddleware()) # Подключаем middleware
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
