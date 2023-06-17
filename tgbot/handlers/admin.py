from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.filters.state import StateFilter

from create_bot import bot
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import AdminInlineKeyboard as inline_kb
from tgbot.keyboards.reply import AdminReplyKeyboard as reply_kb
from tgbot.misc.states import AdminFSM
from tgbot.models.redis_connector import RedisConnector as rds
from tgbot.models.sql_connector import TextsDAO, ServicesDAO

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command("start"))
async def admin_start(message: Message, state: FSMContext):
    text = "Выберите категорию:"
    kb = reply_kb.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.message(F.text == "Управлять контентом")
async def content_management(message: Message):
    text = 'Раздел "Управление контентом".\nВыберите, что вы хотите сделать:'
    kb = inline_kb.content_management_kb()
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "content_management")
async def content_management(callback: CallbackQuery):
    text = 'Раздел "Управление контентом".\nВыберите, что вы хотите сделать:'
    kb = inline_kb.content_management_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


##############
# Редактура текстов авторассылки

@router.callback_query(F.data == "edit_auto_texts")
async def edit_auto_texts(callback: CallbackQuery):
    text = "Выберите контент, который вы хотите изменить:"
    kb = inline_kb.edit_auto_texts_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "auto_text")
async def current_text_clb(callback: CallbackQuery, state: FSMContext):
    chapter = callback.data.split(":")[1]
    current_text = await TextsDAO.get_one_or_none(chapter=chapter)
    if current_text:
        first_msg = current_text["text"]
    else:
        first_msg = "Текст не задан"
    second_msg = "Текущее сообщение ☝️\nОтправьте сообщение, на которое нужно его заменить:"
    kb = inline_kb.current_text_kb()
    await state.update_data(current_text=current_text, chapter=chapter)
    await state.set_state(AdminFSM.auto_texts)
    await callback.message.answer(first_msg)
    await callback.message.answer(second_msg, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(AdminFSM.auto_texts)
async def update_auto_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    current_text = state_data["current_text"]
    chapter = state_data["chapter"]
    if message.content_type == "text":
        new_text = message.html_text
        if current_text:
            await TextsDAO.update(chapter=chapter, text=new_text)
        else:
            await TextsDAO.create(chapter=chapter, text=new_text)
        await state.set_state(AdminFSM.home)
        text = "Выберите контент, который вы хотите изменить:"
        kb = inline_kb.edit_auto_texts_kb()
    else:
        if current_text:
            first_msg = current_text
        else:
            first_msg = "Текст не задан"
        text = "Текущее сообщение ☝️\nОтправьте сообщение, на которое нужно его заменить:"
        kb = inline_kb.current_text_kb()
        await state.update_data(current_text=current_text, chapter=chapter)
        await state.set_state(AdminFSM.auto_texts)
        await message.answer(first_msg)
    await message.answer(text, reply_markup=kb)


##############
# Редактура цен на услуги


@router.callback_query(F.data == "edit_prices")
async def edit_prices(callback: CallbackQuery):
    text = "Выберите вид эпиляции и пол:"
    kb = inline_kb.epil_gender_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "epil_gender")
async def epil_gender(callback: CallbackQuery):
    category = callback.data.split(":")[1].split("|")[0]
    gender = callback.data.split(":")[1].split("|")[1]
    services = await ServicesDAO.get_many(category=category, gender=gender)
    text = "Текущие услуги в боте:"
    kb = inline_kb.services_kb(services=services, category=category, gender=gender)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "new_service")
async def new_service(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[1].split("|")[0]
    gender = callback.data.split(":")[1].split("|")[1]
    category_dict = {"bio": "Био", "laser": "Лазер"}
    gender_dict = {"boys": "Мужчины", "girls": "Девушки"}
    await state.set_state(AdminFSM.new_service)
    await state.update_data(category=category, gender=gender)
    text = f"Создание услуги {category_dict[category]} для {gender_dict[gender]}:\nВведите название услуги, цену в " \
           f"рублях и длительность в минутах через ENTER"
    await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, AdminFSM.new_service)
async def new_service(message: Message, state: FSMContext):
    try:
        service_list = message.text.split("\n")
        title = service_list[0].strip()
        price = int(service_list[1].strip())
        duration = int(service_list[2].strip())
        state_data = await state.get_data()
        category = state_data["category"]
        gender = state_data["gender"]
        await ServicesDAO.create(category=category, gender=gender, title=title, price=price, duration=duration)
        services = await ServicesDAO.get_many(category=category, gender=gender)
        text = "Текущие услуги в боте:"
        kb = inline_kb.services_kb(services=services, category=category, gender=gender)
        await state.set_state(AdminFSM.home)
    except (IndexError, ValueError):
        text = "Вы ввели данные в неверном формате"
        kb = None
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.split(":")[0] == "service_profile")
async def edit_service(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[1])
    service = await ServicesDAO.get_one_or_none(id=service_id)
    if service:
        duration_int = service["duration"]
        duration_str = f"{duration_int // 60}ч {duration_int % 60}мин"
        service_profile = [
            f"{service_id}  <b>{service['title']}</b>",
            f"Цена: <i>{service['price']}₽</i>",
            f"Длительность: <i>{duration_str}</i>\n",
            "Выберите что хотите отредактировать. Если отключить услугу, она станет недоступна для оформления "
            "заказа, но ее можно будет всегда включить\n",
            "<u><b>Функционал кнопок я пока не доделал. Но логика я думаю вам понятна</b></u>"
        ]
        text = "\n".join(service_profile)
        kb = inline_kb.edit_service_kb(service_id=service_id)
    else:
        text = "Что-то пошло не так. Услуга не найдена"
        kb = None
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)





