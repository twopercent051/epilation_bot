from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.utils.markdown import hcode

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import AdminReplyKeyboard as reply_kb
from tgbot.misc.scheduler import PayRegistration2HoursScheduler
from tgbot.misc.states import AdminFSM

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command("test_scheduler"))
async def test_scheduler(message: Message):
    await PayRegistration2HoursScheduler.create(user_id=message.from_user.id)


@router.message(Command("drop_scheduler"))
async def test_scheduler(message: Message):
    await PayRegistration2HoursScheduler.delete(user_id=message.from_user.id)


@router.message(F.sticker)
async def sticker(message: Message):
    await message.answer(f"sticker_id: {hcode(message.sticker.file_id)}")


@router.message(Command("start"))
async def admin_start(message: Message, state: FSMContext):
    text = "Выберите категорию:"
    kb = reply_kb.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)
