from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import AdminReplyKeyboard as reply_kb
from tgbot.misc.states import AdminFSM

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command("start"))
async def admin_start(message: Message, state: FSMContext):
    text = "Выберите категорию:"
    kb = reply_kb.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)
