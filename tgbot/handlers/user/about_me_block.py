import glob
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from tgbot.models.sql_connector import TextsDAO, ClientsDAO, StaticsDAO
from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb

router = Router()


async def girls_feedbacks_choice(user_id: int | str):
    text = "🙌  осталось выбрать о каком виде депиляции вы хотели бы почитать отзывы?"
    kb = inline_kb.feedbacks_categories_kb()
    await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


async def boys_feedback_render(user_id: str | int, page: int, state: FSMContext):
    file_list = await StaticsDAO.get_order_list(category="feedback_boys", like="")
    first_file = (page - 1) * 10
    if len(file_list) - first_file < 11:
        last_file = len(file_list)
        next_page = 1
    else:
        last_file = first_file + 10
        next_page = page + 1
    media_group = []
    for file in file_list[first_file:last_file]:
        photo = file["file_id"]
        media_group.append({"media": photo, "type": "photo"})
    media_msg = await bot.send_media_group(chat_id=user_id, media=media_group)
    await state.update_data(media_msg=media_msg)
    kb = inline_kb.feedbacks_boys_kb(page=next_page)
    await bot.send_message(chat_id=user_id, text="Текст под отзывами", reply_markup=kb)


@router.message(F.text == "Обо мне и отзывы")
@router.message(Command("about_me"))
async def about_me_render(message: Message):
    photo = await TextsDAO.get_one_or_none(chapter="photo|about_me")
    text = await TextsDAO.get_one_or_none(chapter="text|about_me")
    kb = inline_kb.about_me_kb()
    if photo:
        await message.answer_photo(photo=photo["text"])
    else:
        photo = await StaticsDAO.get_one_or_none(title="no_photo")
        await message.answer_photo(photo=photo["file_id"])
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
async def read_feedbacks(callback: CallbackQuery, state: FSMContext):
    user = await ClientsDAO.get_one_or_none(user_id=str(callback.from_user.id))
    if not user:
        return
    if user["gender"] == "boys":
        await boys_feedback_render(page=1, user_id=callback.from_user.id, state=state)
    elif user["gender"] == "girls":
        await girls_feedbacks_choice(user_id=callback.from_user.id)
    elif user["gender"] == "unknown":
        text = "😎  Отзывов у меня очень много. Для вашего удобства я их разделила на  👩‍🦰 ‍  и 👨   , и сделала 2 " \
               "категории. Выбирайте пожалуйста интересную вам ☘"
        kb = inline_kb.feedbacks_gender_kb()
        await callback.message.answer(text, reply_markup=kb)


@router.callback_query(F.data.split("|")[0] == "feedbacks_boys")
async def refresh_feedback_boys(callback: CallbackQuery, state: FSMContext):
    page = callback.data.split("|")[1].split(":")[1]
    page = 1 if page == "start" else int(page)
    if page == "start":
        page = 1
    else:
        page = int(page)
        state_data = await state.get_data()
        media_msg_list = state_data["media_msg"]
        for media_msg in media_msg_list:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=media_msg.message_id)
    await callback.message.delete()
    await boys_feedback_render(user_id=callback.from_user.id, page=page, state=state)
    await bot.answer_callback_query(callback.id)
