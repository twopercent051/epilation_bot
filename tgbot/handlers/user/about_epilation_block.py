import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, CallbackQuery

from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb
from create_bot import bot

router = Router()


async def epilation_diff(user_id: int | str):
    photo = FSInputFile(path=f'{os.getcwd()}/tgbot/static/epilation_diff.jpg')
    text_1 = "<b>БИО</b>\n- 5-20 минут и ваша кожа гладкая и шелковистая до 21 дня,\n- ощущение ухоженности и " \
             "уверенности  24/7\n- отрастающий волос становится мягче, реже, светлее\n- нет раздражения, чесотки, " \
             "щетины, прыщей\n- процедура занимает от 5 до 30 минут 1 раз в месяц\n- нет порезов\n- можно " \
             "использовать в области тату\n- натуральные компоненты в составе материалов\n- процедура ощутима, " \
             "но терпима.\n- кожа в процессе депиляции пилингуется и становится бархатистой и " \
             "нежной\n\n<b>ЛАЗЕР</b>\n- не нужно отращивать волосы\n- постоянная гладкость в течении 3-10 лет после " \
             "курса из 6-12 процедур\n- лазерный луч разрушает волосяной фолликул и волос долго не растёт\n- " \
             "процедура занимает от 5 до 30 минут\n- нет раздражения, чесотки, щетины, прыщей\n- процедура " \
             "безболезненна\n- волосы не врастают\n- вросшие волосы и пятна от вросших проходят\n- Soprano Titanium " \
             "можно использовать на загорелой коже\n\n<b>БРИТВА/КРЕМ</b>\n- гладкость до 24 часов;\n- процедура " \
             "отнимает 15 минут ежедневно;\n- вызывает раздражение, чесотку, покраснения, прыщи, щетину врастание " \
             "волос\n- волосы после боится всегда растут жесткие, грубые, колючие и густые\n- кожа выглядит " \
             "неопрятно\n- возможны болезненные порезы"
    text_2 = "Вам надоело ежедневное бритье и его последствия в виде раздражения, щетины и жесткости волос?😫\nВы " \
             "хотите гладкости и опрятности, надолго?\nВам в раздел➡ *Подробнее о лазерной эпиляции*.\n\nЕсли вам " \
             "хочется временного удаления волос с результатом за 21 день, кликайте на ➡*Подробнее о " \
             "биоэпиляции*.\n\nВ каждом разделе я постаралась коротко и без воды рассказать вам самое главное!"
    kb = inline_kb.about_epilation_kb()
    await bot.send_photo(chat_id=user_id, photo=photo)
    await bot.send_message(chat_id=user_id, text=text_1)
    await bot.send_message(chat_id=user_id, text=text_2, reply_markup=kb)


@router.message(F.text == "Коротко о видах эпиляции")
@router.message(Command("information"))
async def about_epilation(message: Message):
    await message.delete()
    await epilation_diff(user_id=message.from_user.id)


@router.callback_query(F.data == "epil_diff")
async def about_epilation(callback: CallbackQuery):
    await epilation_diff(user_id=callback.from_user.id)
    await bot.answer_callback_query(callback.id)

