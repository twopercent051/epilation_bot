import asyncio

from tgbot.handlers.admin.admin import router as admin_router
from tgbot.handlers.admin.content_management import router as content_router
from tgbot.handlers.user.registration_block import router as registration_block
from tgbot.handlers.user.price_block import router as price_block
from tgbot.handlers.echo import router as echo_router
from tgbot.misc.scheduler import scheduler_jobs
from tgbot.models.redis_connector import RedisConnector as rds

from create_bot import bot, dp, scheduler, logger, register_global_middlewares, config

admin_routers = [
    admin_router,
    content_router
]

user_routers = [
    registration_block,
    price_block
]


async def main():
    logger.info("Starting bot")
    scheduler_jobs()
    rds.redis_start()
    dp.include_routers(
        # *admin_routers,
        *user_routers,
        echo_router)

    try:
        scheduler.start()
        register_global_middlewares(dp, config)
        # await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        scheduler.shutdown(True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
