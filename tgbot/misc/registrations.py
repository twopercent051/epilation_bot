from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from create_bot import bot, dp
from tgbot.handlers.user.registration_block import UserMainMenu
from tgbot.models.sql_connector import RegistrationsDAO


async def create_registration(data: dict, phone: str, user_id: str | int, advance="not_required") -> int:
    start_time = data["reg_time"]
    finish_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=data["duration"])).time()
    services_ids = []
    for service in data["services"]:
        services_ids.append(service["id"])
    registration = await RegistrationsDAO.create(
        reg_date=data["reg_date"],
        reg_time_start=start_time,
        reg_time_finish=finish_time,
        services=services_ids,
        total_price=data["price"],
        phone=phone,
        user_id=str(user_id),
        advance=advance
    )
    return registration["id"]


async def cancel_registration(user_id: int | str, reg_id: int):
    await RegistrationsDAO.update(reg_id=reg_id, status="cancelled")
    text = "Запись отменена"
    state_with: FSMContext = FSMContext(
        bot=bot,
        storage=dp.storage,
        key=StorageKey(
            chat_id=user_id,
            user_id=user_id,
            bot_id=bot.id
        )

    )
    state = await state_with.get_state()
    await bot.send_message(chat_id=user_id, text=text)
    await UserMainMenu.menu_type(user_id=user_id, state=state)
