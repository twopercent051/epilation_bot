from aiogram.fsm.state import State, StatesGroup


class AdminFSM(StatesGroup):
    home = State()
    auto_texts = State()
    new_service = State()
    edit_service = State()

    # info block
    address_video = State()
    address_location = State()
    address_text = State()

    about_me_video = State()
    about_me_photo = State()
    about_me_text = State()

    price_list_photo = State()


class UserFSM(StatesGroup):
    home = State()
    manual_phone = State()
    full_name = State()
    birthday = State()

    main_menu = State()
