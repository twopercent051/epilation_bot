from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from tgbot.models.sql_connector import TextsDAO, ClientsDAO
from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb

router = Router()


async def girls_feedbacks_render(user_id: int | str):
    text = "🙌  осталось выбрать о каком виде депиляции вы хотели бы почитать отзывы?"
    kb = inline_kb.feedbacks_categories_kb()
    await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


@router.message(F.text == "Обо мне и отзывы")
@router.message(Command("about_me"))
async def about_me_render(message: Message):
    photo = await TextsDAO.get_one_or_none(chapter="photo|about_me")
    text = await TextsDAO.get_one_or_none(chapter="text|about_me")
    kb = inline_kb.about_me_kb()
    if photo:
        await message.answer_photo(photo=photo["text"])
    if text:
        await message.answer(text=text["text"])
    else:
        await message.answer(text="ТЕКСТ ОТСУТСТВУЕТ", reply_markup=kb)


@router.callback_query(F.data == "about_me_video")
async def about_me_video(callback: CallbackQuery):
    video = await TextsDAO.get_one_or_none(chapter="video|about_me")
    kb = inline_kb.about_me_kb()
    if video:
        await callback.message.answer_video(video=video["text"], reply_markup=kb)
    else:
        await callback.message.answer(text="ВИДЕО ОТСУТСТВУЕТ", reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "read_feedbacks")
async def read_feedbacks(callback: CallbackQuery):
    user = await ClientsDAO.get_one_or_none(user_id=str(callback.from_user.id))
    if not user:
        return
    if user["gender"] == "boys":
        print(str(callback.from_user.id))
        pass
    elif user["gender"] == "girls":
        await girls_feedbacks_render(user_id=callback.from_user.id)
    elif user["gender"] == "unknown":
        text = "😎  Отзывов у меня очень много. Для вашего удобства я их разделила на  👩‍🦰 ‍  и 👨   , и сделала 2 " \
               "категории. Выбирайте пожалуйста интересную вам ☘"
        kb = inline_kb.feedbacks_gender_kb()
        await callback.message.answer(text, reply_markup=kb)



