import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load cookies from the file
def load_cookies(filename):
    with open(filename, 'r') as f:
        cookies = json.load(f)
    return cookies

# Download video from a YouTube URL
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0]  # Get URL from command arguments
    if not url:
        await update.message.reply_text("Please provide a YouTube URL.")
        return

    # Set up yt-dlp options
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt',  # Path to your cookies file
        'outtmpl': '%(title)s.%(ext)s',  # File naming
    }

    async with context.bot.chat_data as data:
        try:
            await update.message.reply_text("Downloading video...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await update.message.reply_text("Download completed.")
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            await update.message.reply_text("An error occurred while downloading the video.")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send a YouTube video URL to download it.")

# Main function to run the bot
if __name__ == '__main__':
    # Load your API ID, API Hash, and Bot Token
    API_ID = '22420997'  # Replace with your API ID
    API_HASH = 'd7fbe2036e9ed2a1468fad5a5584a255'  # Replace with your API Hash
    BOT_TOKEN = '7410410018:AAEM-Rbf9b6SVS3PsYcm1fNkkISTas2Fch0'  # Replace with your Bot Token

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Load cookies (optional, if needed)
    cookies = load_cookies('cookies.txt')

    # Run the bot
    application.run_polling()
