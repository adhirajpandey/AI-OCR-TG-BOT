from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from io import BytesIO
import numpy as np
import cv2

from ai_ocr import AI_ocr

import requests

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}!, I am a AI assisted OCR Bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"I am a AI assisted OCR Bot, please send a photo to me and I will try to provide the correct text in the photo")


async def ocr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"This is the main command for OCR function")


# Responses
async def handle_response(text: str):
    if text == "Hello":
        return "Hi"
    else:
        return "I don't understand"


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the photo file from the update
    photo = update.message.photo[-1]
    # Get the file object for the photo
    file_info = await context.bot.get_file(photo.file_id)

    # Construct the download URL and download the image
    download_url = file_info.file_path
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open("D:\downloaded_image.jpg", 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        ai_ocr_result = AI_ocr(r"D:\downloaded_image.jpg")
        await update.message.reply_text(ai_ocr_result)
        # await update.message.reply_text("Image downloaded successfully!")
    else:
        await update.message.reply_text("Failed to download the image.")

    # ocr_result = await AI_ocr(img)
    # await update.message.reply_text(ocr_result)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response = await handle_response(text)

    print(f'Bot: "{response}"')

    await update.message.reply_text(response)


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TG_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ocr", ocr_command))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling...")
    app.run_polling(poll_interval=3)
