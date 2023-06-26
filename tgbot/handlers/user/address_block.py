from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from tgbot.models.sql_connector import TextsDAO

router = Router()


async def address_render(user_id: int | str):
    video = await TextsDAO.get_one_or_none(chapter="video|address")
    text = await TextsDAO.get_one_or_none(chapter="text|address")
    location = await TextsDAO.get_one_or_none(chapter="location|address")
    if video:
        await bot.send_video(chat_id=user_id, video=video["text"])
    if text:
        await bot.send_message(chat_id=user_id, text=text["text"])
    if location:
        latitude = location["text"].split("|")[1]
        longitude = location["text"].split("|")[0]
        await bot.send_location(chat_id=user_id, latitude=latitude, longitude=longitude)


@router.message(Command("address"))
@router.message(F.text == "Адрес")
async def address(message: Message):
    await address_render(user_id=message.from_user.id)
    await message.delete()


@router.callback_query(F.data == "address")
async def address(callback: CallbackQuery):
    await address_render(user_id=callback.from_user.id)
    await bot.answer_callback_query(callback.id)

