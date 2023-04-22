async def on_startup(dp):

    # подгружаем фильтры
    import filters
    filters.setup(dp)

    # подгружаем middlewares
    import middlewares
    middlewares.setup(dp)

    # уведомляем администраторов о запуске
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    # устанавливаем команды
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print("Бот запущен")

if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
