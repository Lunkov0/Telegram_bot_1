import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from commands import commands

from handlers import start, make_appointment, admin
from handlers.admin_hl import schedule, schedule_changes, treatments


async def main() -> None:
    # bot = Bot(token=os.getenv('TOKEN'))
    bot = Bot('6679199342:AAH2CHgDn0mpdhXLs34SwIhJRopWgOybvXI')
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(make_appointment.router)
    dp.include_router(admin.router)
    dp.include_router(schedule.router)
    dp.include_router(schedule_changes.router)
    dp.include_router(treatments.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
