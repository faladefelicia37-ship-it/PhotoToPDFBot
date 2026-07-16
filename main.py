import os
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Replace with your BotFather token
import os

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Welcome!\n\nSend me a picture and I'll convert it into a PDF."
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the highest resolution photo
        photo = update.message.photo[-1]
        file = await photo.get_file()

        image_file = "image.jpg"
        pdf_file = "converted.pdf"

        # Download image
        await file.download_to_drive(image_file)

        # Convert image to PDF
        image = Image.open(image_file)

        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(pdf_file, "PDF")

        # Send PDF
        with open(pdf_file, "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="converted.pdf",
                caption="✅ Your PDF is ready!"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")

    finally:
        # Delete temporary files
        if os.path.exists("image.jpg"):
            os.remove("image.jpg")

        if os.path.exists("converted.pdf"):
            os.remove("converted.pdf")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
