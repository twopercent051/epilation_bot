from typing import Literal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminInlineKeyboard:
    """Клавиатура админа"""

    @classmethod
    def content_management_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Изменить тексты автоматических рассылок", callback_data='edit_auto_texts')],
            [InlineKeyboardButton(text="Изменить цены услуг", callback_data='edit_prices')],
            [InlineKeyboardButton(text="Изменить информационные блоки", callback_data='edit_info_blocks')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_auto_texts_kb(cls):
        kb_data = [
            {"kb_title": "На Новый год", "clb_data": "new_year"},
            {"kb_title": "На 23 февраля", "clb_data": "23_february"},
            {"kb_title": "На день рождения - за неделю", "clb_data": "1week_before_birthday"},
            {"kb_title": "На день рождения - в день рождения", "clb_data": "at_birthday"},
            {"kb_title": "За 24 часа до приёма - новым клиентам", "clb_data": "before_24h_new"},
            {"kb_title": "За 24 часа до приёма - текущим клиентам", "clb_data": "before_24h_old"},
            {"kb_title": "За 2 часа до приёма", "clb_data": "before_2h"},
            {"kb_title": "Через 3 часа после процедуры - Био", "clb_data": "after_3h_bio"},
            {"kb_title": "Через 3 часа после процедуры - Лазер", "clb_data": "after_3h_laser"},
            {"kb_title": "Через 3+2 часа после процедуры", "clb_data": "after_5h"},
            {"kb_title": "Через 1 месяц после приёма", "clb_data": "after_1m"},
            {"kb_title": "Через 3 месяца после приёма", "clb_data": "after_3m"},
        ]
        keyboard = []
        for button in kb_data:
            keyboard.append([InlineKeyboardButton(text=button["kb_title"],
                                                  callback_data=f"auto_text:{button['clb_data']}")])
        keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="content_management")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def current_text_kb(cls):
        keyboard = [[InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_auto_texts")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def epil_gender_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Биоэпиляция - девушки", callback_data="epil_gender:bio|girls")],
            [InlineKeyboardButton(text="Биоэпиляция - мужчины", callback_data="epil_gender:bio|boys")],
            [InlineKeyboardButton(text="Лазерная эпиляция - девушки", callback_data="epil_gender:laser|girls")],
            [InlineKeyboardButton(text="Лазерная эпиляция - мужчины", callback_data="epil_gender:laser|boys")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="content_management")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def services_kb(cls, services: list, category: str, gender: str):
        keyboard = []
        for service in services:
            enable_dict = {"enabled": "", "disabled": "🚫"}
            category_dict = {"bio": "Био", "laser": "Лазер"}
            gender_dict = {"boys": "Мужчины", "girls": "Девушки"}
            duration_int = service["duration"]
            duration_str = f"{duration_int // 60}ч {duration_int % 60}мин"
            text_button = f"{enable_dict[service['status']]} {service['ordering']} {gender_dict[gender]} - " \
                          f"{category_dict[category]} - {service['title']} - {service['price']}₽ - {duration_str}"
            keyboard.append([InlineKeyboardButton(text=text_button, callback_data=f"service_profile:{service['id']}")])
        keyboard.append([InlineKeyboardButton(text="🆕 Создать услугу",
                                              callback_data=f"new_service:{category}|{gender}")])
        keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_prices")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_service_kb(cls, service_id: int, status: str, gender: str, category: str):
        status_dict = {"enabled": "🚫 Скрыть", "disabled": "Показать"}
        keyboard = [
            [
                InlineKeyboardButton(text="📄 Название", callback_data=f"edit_service:{service_id}|title"),
                InlineKeyboardButton(text="💰 Цена", callback_data=f"edit_service:{service_id}|price"),
            ],
            [
                InlineKeyboardButton(text="⏳ Длительность", callback_data=f"edit_service:{service_id}|duration"),
                InlineKeyboardButton(text="↗️ Порядок в списке", callback_data=f"edit_service:{service_id}|ordering"),
            ],
            [InlineKeyboardButton(text=status_dict[status],
                                  callback_data=f"edit_service_status:{service_id}|{status_dict[status]}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"epil_gender:{category}|{gender}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_info_block_kb(cls):
        keyboard = [
            [
                InlineKeyboardButton(text="Адрес", callback_data="edit_info_block:address"),
                InlineKeyboardButton(text="Обо мне", callback_data="edit_info_block:about_me"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="content_management"),
                InlineKeyboardButton(text="Прайс лист", callback_data="edit_info_block:price_list"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_address_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Видео от остановки до кабинета", callback_data="edit_address:video")],
            [InlineKeyboardButton(text="Геометка", callback_data="edit_address:location")],
            [InlineKeyboardButton(text='Текст "Адрес"', callback_data="edit_address:text")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_info_blocks")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_about_me_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Приветственное видео", callback_data="edit_about_me:video")],
            [InlineKeyboardButton(text="Фото мастера", callback_data="edit_about_me:video")],
            [InlineKeyboardButton(text='Текст "Обо мне"', callback_data="edit_about_me:video")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_info_blocks")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_price_list_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Картинка-прайс - Био - Мужчины", callback_data="edit_price:bio_boys")],
            [InlineKeyboardButton(text="Картинка-прайс - Био - Девушки", callback_data="edit_price:bio_girls")],
            [InlineKeyboardButton(text="Картинка-прайс - Лазер - Мужчины", callback_data="edit_price:laser_boys")],
            [InlineKeyboardButton(text="Картинка-прайс - Лазер - Девушки", callback_data="edit_price:laser_girls")],
            [InlineKeyboardButton(text="Картинка-прайс - Био - Абонементы", callback_data="edit_price:bio_abonements")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_info_blocks")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_info_block_back_kb(cls, chapter: str):
        keyboard = [[InlineKeyboardButton(text="⬅️ Назад", callback_data=f"edit_info_block:{chapter}")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class UserInlineKeyboard:
    """Клавиатура пользователя"""

    @classmethod
    def phone_in_base_kb(cls, phone):
        keyboard = [
            [InlineKeyboardButton(text="Отправить Оксане уведомление", callback_data=f"msg_to_admin|{phone}")],
            [InlineKeyboardButton(text="Хочу ввести другой телефон", callback_data="correct_phone")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def user_gender_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Мужчина", callback_data="user_gender:boys")],
            [InlineKeyboardButton(text="Девушка", callback_data="user_gender:girls")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def user_birthday_kb(cls):
        keyboard = [[InlineKeyboardButton(text="Не хочу вводить дату рождения", callback_data="main_menu")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def price_gender_kb(cls, gender: Literal["boys", "girls"]):
        if gender == "boys":
            keyboard = [[InlineKeyboardButton(text="Посмотреть прайс для девушек 👩‍🦰",
                                              callback_data="price_gender:girls")]]
        else:
            keyboard = [[InlineKeyboardButton(text="Посмотреть прайс для мужчин 👨",
                                              callback_data="price_gender:boys")]]
        keyboard.append([InlineKeyboardButton(text="Посмотреть сравнение видов эпиляции", callback_data="epil_diff")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
