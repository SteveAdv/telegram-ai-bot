import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Hugging Face pipeline for conversational AI
chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your AI bot. Type /help to see the available commands.')

# Help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/start - Start the conversation\n/help - Show this help message\n/ask <question> - Ask the AI a question')

# Command to ask the AI a question
def ask(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input:
        response = chatbot(user_input)
        update.message.reply_text(response[0]['generated_text'])
    else:
        update.message.reply_text('Please provide a question after /ask.')

# Message handler for echoing messages
def echo(update: Update, context: CallbackContext) -> None:
    response = chatbot(update.message.text)
    update.message.reply_text(response[0]['generated_text'])

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update %s caused error %s', update, context.error)

# Main function to run the bot
if __name__ == '__main__':
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN')  # Add your Telegram bot token here

    dp = updater.dispatcher
    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('ask', ask))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # Register error handler
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()