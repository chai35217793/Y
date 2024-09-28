import logging
import os
import json
from pytube import YouTube
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your API credentials
API_ID = 22420997
API_HASH = 'd7fbe2036e9ed2a1468fad5a5584a255'
BOT_TOKEN = '7410410018:AAEM-Rbf9b6SVS3PsYcm1fNkkISTas2Fch0'

# Load cookies
def load_cookies(filename):
    with open(filename, 'r') as f:
        cookies = json.load(f)
    return cookies

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Send me a YouTube video URL to download.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send a YouTube video URL to download it.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video_file = video.download()  # Download the video
        await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_file, 'rb'))
        os.remove(video_file)  # Clean up the file after sending
    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')

def main() -> None:
    # Load cookies if necessary
    cookies = load_cookies('cookies.txt')  # Adjust the path as needed

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    application.run_polling()

if __name__ == '__main__':
    main()
