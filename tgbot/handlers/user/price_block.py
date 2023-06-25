from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from tgbot.misc.states import UserFSM
from tgbot.models.sql_connector import RegistrationsDAO, TextsDAO
from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb

router = Router()


async def price_render(user_id: int | str, gender: str):
    laser_photo = await TextsDAO.get_one_or_none(chapter=f"laser_{gender}|price_list")
    bio_photo = await TextsDAO.get_one_or_none(chapter=f"bio_{gender}|price_list")
    bio_abonements = await TextsDAO.get_one_or_none(chapter="bio_abonements|price_list")
    laser_photo = laser_photo["text"] if laser_photo is not None else "AgACAgIAAxkBAAIc62SRHzWI3vScUToj2Ef5pa_pn32KAAIqyzEb_kKISO-bIsonmGRFAQADAgADeQADLwQ"
    bio_photo = bio_photo["text"] if bio_photo is not None else "AgACAgIAAxkBAAIc62SRHzWI3vScUToj2Ef5pa_pn32KAAIqyzEb_kKISO-bIsonmGRFAQADAgADeQADLwQ"
    bio_abonements = bio_abonements["text"] if bio_abonements is not None else "AgACAgIAAxkBAAIc62SRHzWI3vScUToj2Ef5pa_pn32KAAIqyzEb_kKISO-bIsonmGRFAQADAgADeQADLwQ"
    kb = inline_kb.price_gender_kb(gender=gender)
    await bot.send_photo(chat_id=user_id, photo=laser_photo)
    await bot.send_photo(chat_id=user_id, photo=bio_photo)
    await bot.send_photo(chat_id=user_id, photo=bio_abonements, reply_markup=kb)


@router.message(F.text == "Прайс", UserFSM.main_menu)
async def price_list(message: Message):
    finished_registrations = await RegistrationsDAO.get_by_user_id(user_id=str(message.from_user.id))
    if len(finished_registrations) == 0:
        pass
    await price_render(user_id=message.from_user.id, gender="girls")


@router.callback_query(F.data.split(":")[0] == "price_gender")
async def price_list(callback: CallbackQuery):
    gender = callback.data.split(":")[1]
    await price_render(gender=gender, user_id=callback.from_user.id)
    await bot.answer_callback_query(callback.id)
