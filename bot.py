import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import openai
import requests
from io import BytesIO

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your AI image bot. Use /create <description> to generate an image.')

# Command handler for /create
def create(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text('Please provide a description after /create.')
        return

    description = ' '.join(context.args)
    update.message.reply_text(f'Generating image for: {description}...')
    
    image_url = generate_image(description)

    if image_url:
        response = requests.get(image_url)
        bio = BytesIO(response.content)
        bio.seek(0)
        update.message.reply_photo(photo=InputFile(bio, filename="generated_image.png"))
    else:
        update.message.reply_text('Failed to generate image.')

def generate_image(description):
    openai.api_key = 'sk-proj-CmhXycL4VooxwdMCWp2FT3BlbkFJSDJXCV5i7B6ugwGv0tOd'
    try:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None

def main() -> None:
    # Insert your bot token here
    token = '6996555789:AAEiH5R9wZmSYdIn9iG4wlVzVB9u2EBMVEE'

    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create", create))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
