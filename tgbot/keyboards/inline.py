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
            [InlineKeyboardButton(text="Фото мастера", callback_data="edit_about_me:photo")],
            [InlineKeyboardButton(text='Текст "Обо мне"', callback_data="edit_about_me:text")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_info_blocks")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edit_price_list_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Картинка для новых клиентов", callback_data="edit_price:new_clients")],
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
    def phone_in_base_kb(cls, phone: str):
        keyboard = [
            [InlineKeyboardButton(text="Отправить Оксане уведомление", callback_data=f"msg_to_admin|{phone}")],
            [InlineKeyboardButton(text="Хочу ввести другой телефон", callback_data="correct_phone")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def answer_to_user_kb(cls, user_id: str | int):
        keyboard = [[InlineKeyboardButton(text="↩️ Ответить", callback_data=f"answer:{user_id}")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def msg_to_admin_kb(cls):
        keyboard = [[InlineKeyboardButton(text="Написать Оксане в ЛС", url="https://t.me/neprostowaxing")]]
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

    @classmethod
    def about_epilation_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Подробнее о лазерной эпиляции", callback_data="about_epil:laser")],
            [InlineKeyboardButton(text="Подробнее о биоэпиляции (шугаринг/воск)", callback_data="about_epil:bio")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def about_me_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Посмотреть приветственное видео", callback_data="about_me_video")],
            [InlineKeyboardButton(text="Читать отзывы", callback_data="read_feedbacks")],
            [InlineKeyboardButton(text="Написать Оксане в личку", url="https://t.me/neprostowaxing")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedbacks_categories_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Отзывы о лазерной эпиляции", callback_data="feedbacks_laser")],
            [InlineKeyboardButton(text="Отзывы о биоэпиляции (воск/шугаринг)", callback_data="feedbacks_bio")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedbacks_gender_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Отзывы от мужчин", callback_data="feedbacks_boys|page:start")],
            [InlineKeyboardButton(text="Отзывы от девушек", callback_data="feedbacks_girls")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedbacks_boys_kb(cls, page: str | int):
        keyboard = [
            [InlineKeyboardButton(text="Читать ещё", callback_data=f"feedbacks_boys|page:{page}")],
            [InlineKeyboardButton(text="Отзывы от девушек 👩‍🦰", callback_data="feedbacks_girls")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class UserAboutEpilationInline:

    @classmethod
    def laser_boys_1_kb(cls):
        keyboard = [
            [
                InlineKeyboardButton(text="Для девушки 👩‍🦰", callback_data="about_epil:laser:girls:1"),
                InlineKeyboardButton(text="Далее ➡️", callback_data="about_epil:laser:boys:2"),

            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def laser_boys_2_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Часто задаваемые вопросы от мужчин ❔", callback_data="about_epil:laser:boys:3")],
            [InlineKeyboardButton(text="Отзывы от мужчин", callback_data="feedbacks_boys|page:start")],
            [InlineKeyboardButton(text="Хочу записаться на процедуру", callback_data="sign_up")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def laser_boys_3_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Хочу записаться на процедуру 📝", callback_data="sign_up")],
            [InlineKeyboardButton(text="Ок. С лазерной понятно, хочу почитать про биоэпиляцию",
                                  callback_data="about_epil:bio")],
            [InlineKeyboardButton(text="Написать Оксане в личку", url="https://t.me/neprostowaxing")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def bio_boys_1_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Часто задаваемые вопросы от мужчин ❔", callback_data="about_epil:bio:boys:2")],
            [InlineKeyboardButton(text="Читать про биоэпиляцию для девушки", callback_data="about_epil:bio:girls:1")],
            [
                InlineKeyboardButton(text="Отзывы", callback_data="feedbacks_boys|page:start"),
                InlineKeyboardButton(text="Записаться 📝", callback_data="sign_up"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def bio_boys_2_kb(cls):
        keyboard = [
            [
                InlineKeyboardButton(text="Отзывы", callback_data="feedbacks_boys|page:start"),
                InlineKeyboardButton(text="Записаться 📝", callback_data="sign_up"),
            ],
            [InlineKeyboardButton(text="Ок. С биоэпиляцией понятно, хочу почитать про лазерную",
                                  callback_data="about_epil:laser:boys:1")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def laser_girls_1_kb(cls):
        keyboard = [
            [
                InlineKeyboardButton(text="Для мужчины 🧑", callback_data="about_epil:laser:boys:1"),
                InlineKeyboardButton(text="Далее ➡️", callback_data="about_epil:laser:girls:2"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def laser_girls_2_kb(cls):
        keyboard = [
            [
                # todo Исправить коллбек дату
                InlineKeyboardButton(text="Отзывы", callback_data="feedbacks_girls|page:start"),
                InlineKeyboardButton(text="Записаться 📝", callback_data="sign_up"),
            ],
            [InlineKeyboardButton(text="Часто задаваемые вопросы ❔", callback_data="about_epil:laser:girls:3")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def laser_girls_3_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Хочу записаться на процедуру 📝", callback_data="sign_up")],
            [InlineKeyboardButton(text="Ок. С лазерной понятно, хочу почитать про биоэпиляцию",
                                  callback_data="about_epil:bio")],
            [InlineKeyboardButton(text="Написать Оксане в личку", url="https://t.me/neprostowaxing")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def bio_girls_1_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Часто задаваемые вопросы от девушек ❔", callback_data="about_epil:bio:girls:2")],
            [InlineKeyboardButton(text="Читать про биоэпиляцию для мужчин", callback_data="about_epil:bio:boys:1")],
            [
                # todo Исправить коллбек дату
                InlineKeyboardButton(text="Отзывы", callback_data="feedbacks_boys|page:start"),
                InlineKeyboardButton(text="Записаться 📝", callback_data="sign_up"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def bio_girls_2_kb(cls):
        keyboard = [
            [
                # todo Исправить коллбек дату
                InlineKeyboardButton(text="Отзывы", callback_data="feedbacks_boys|page:start"),
                InlineKeyboardButton(text="Записаться 📝", callback_data="sign_up"),
            ],
            [InlineKeyboardButton(text="Ок. С биоэпиляцией понятно, хочу почитать про лазерную",
                                  callback_data="about_epil:laser:girls:1")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
