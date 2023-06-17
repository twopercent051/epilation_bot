from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class AdminReplyKeyboard:
    """Клавиатура админа (реплай)"""

    @classmethod
    def main_menu_kb(cls):
        kb = [
            [KeyboardButton(text="Необходимая рутина")],
            [KeyboardButton(text="Управлять контентом")],
            [KeyboardButton(text="Расписание")],
            [KeyboardButton(text="Клиенты")],
            [KeyboardButton(text="Массовое сообщение")],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=False)
        return keyboard


class UserReplyKeyboard:
    """Клавиатура юзера для передачи телефона"""

    @classmethod
    def phone_keyboard(cls):
        kb = [
            [
                KeyboardButton(text='Поделиться телефоном автоматически', request_contact=True),
                KeyboardButton(text='Ввести телефон вручную')
            ],
            [KeyboardButton(text='В начало')],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
