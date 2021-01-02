import logging
import os
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.config import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('''Hi, I am backdoor to your servers.
    You can use me to run commands on your servers,
    but before that I should be running on your servers.''')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""You don't necessarily need a computer to run commands on your servers.
    I am backdoor to your servers. you can send me a command that you want to run on your server,
    I will execute the commands and return you the result. but before that I should be running on your servers.
    I am open source and free telegram bot. Please clone my github repo to start using me. for more information please
    visit https://www.github.com/grsoratoor""")


def run_cmd(update, context):
    """Echo the user message."""
    cmd = update.message.text
    process = subprocess.run(['echo', 'hi'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        update.message.reply_text(stdout)
    if stderr:
        update.message.reply_text(stderr)


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, run_cmd))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
