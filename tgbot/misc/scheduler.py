from datetime import datetime, timedelta

from create_bot import scheduler, bot, config
from tgbot.handlers.user.registration_block import UserMainMenu
from tgbot.keyboards.inline import UserSignUpInline

admin_ids = config.tg_bot.admin_ids


class BaseScheduler:
    event_type = None

    @classmethod
    async def delete(cls, reg_id: int):
        scheduler.remove_job(job_id=f"{reg_id}_{cls.event_type}")


class PayRegistration2HoursScheduler(BaseScheduler):
    event_type = "reg2hours"

    @classmethod
    async def func(cls, user_id: str | int, reg_id: int):
        text = 'К сожалению, не удалось подтвердить оплату.\nЕсли вы уверены, что оплата прошла, то пожалуйста срочно ' \
               'свяжитесь с Оксаной. Либо нажмите "Написать Оксане", либо позвоните по номеру +79117737477.\nЕсли вы ' \
               'передумали, то прошу нажать "Отменить запись ❌" или запись через 1 час отменится автоматически.'
        kb = UserSignUpInline.pay_advance_kb(reg_id=reg_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)
        await PayRegistration1HourScheduler.create(user_id=user_id)

    @classmethod
    async def create(cls, user_id: str | int, reg_id: int):
        dtime = datetime.utcnow() + timedelta(hours=2)
        scheduler.add_job(
            id=f"{reg_id}_{cls.event_type}",
            func=cls.func,
            trigger="date",
            run_date=dtime,
            kwargs={
                "user_id": user_id,
                "reg_id": reg_id
            }
        )


class PayRegistration1HourScheduler(BaseScheduler):
    event_type = "reg1hour"

    @classmethod
    async def func(cls, user_id: str | int, reg_id: int):
        await UserMainMenu.menu_type()

    @classmethod
    async def create(cls, user_id: str | int, reg_id: int):
        dtime = datetime.utcnow() + timedelta(hours=1)
        scheduler.add_job(
            id=f"{reg_id}_{cls.event_type}",
            func=cls.func,
            trigger="date",
            run_date=dtime,
            kwargs={
                "user_id": user_id,
                "reg_id": reg_id
            }
        )
