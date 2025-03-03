# -*- coding: utf-8 -*-

import asyncio

from app.handlers import router
from bot_dp import bot, dp


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')