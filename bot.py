import asyncio
import time
import nest_asyncio
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config

# Применяем nest_asyncio, чтобы разрешить вложенные event loop
nest_asyncio.apply()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаем кнопку, открывающую веб-приложение внутри Telegram
    webapp = WebAppInfo(url=config.WEBAPP_URL)
    button = InlineKeyboardButton(text="Запустить казино", web_app=webapp)
    keyboard = InlineKeyboardMarkup([[button]])
    
    await update.message.reply_text(
        "Добро пожаловать в Мини-Казино! Нажмите кнопку ниже для игры.",
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используйте кнопку 'Запустить казино' для входа в игру.")

async def main() -> None:
    # Создаем приложение с использованием токена из config.py
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Запускаем бота в режиме polling
    await application.run_polling()

if __name__ == '__main__':
    try:
        # Попытка получить уже запущенный event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Если event loop уже запущен (например, в VS Code или Jupyter),
        # то создаем задачу и не завершаем программу, чтобы бот продолжал работать.
        asyncio.create_task(main())
        # Оставляем скрипт активным
        while True:
            time.sleep(1)
    else:
        # Если event loop не запущен, запускаем стандартно
        asyncio.run(main())