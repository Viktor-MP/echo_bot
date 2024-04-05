import os
from dotenv import load_dotenv
from typing import Final
# Telegram imports
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN: Final = os.getenv("echoBotToken")
BOT_USERNAME: Final = os.getenv("echoBotName")


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello you pressed start Button")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Im reCaller_bot. So type something")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom command")


# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    response = text
    if processed == "hello":
        response = "Hey there!"
    elif processed == "how are you":
        response = "I'm good!"
    elif response == "i love python":
        response = "Remember to subscribe"

    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in ({message_type}): '{text}'")
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print(f"Bot: {response}")
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update: {update} caused err: {context.error}")


# print(__name__)
# print(TOKEN)
# print(BOT_USERNAME)

if __name__ == "__main__":
    print("Start bot ...")
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # How often to update bot for getting new messages
    print("polling...")
    app.run_polling(poll_interval=3)