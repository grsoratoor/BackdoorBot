import logging
import pexpect
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.config import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('''
Hi, I am backdoor to your servers.
You can use me to run commands on your servers,
but before that I should be running on your servers.
''')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
You don't necessarily need a computer to run commands on your servers.
I am backdoor to your servers. you can send me a command that you want to run on your server,
I will execute the commands and return you the result. but before that I should be running on your servers.
I am open source and free telegram bot. Please clone my github repo to start using me. for more information please
visit https://www.github.com/grsoratoor
    
Available Commands
/start - starts the bot
/new_session - Creates new backdoor session
/end_session - Ends existing session
/help - shows this message
""")


def new_session(update, context):
    """Start new session"""
    global child
    if child:
        child.kill(0)
    child = pexpect.spawn('/bin/bash')
    child.expect('\$')
    output = "Backdoor session created"
    update.message.reply_text(output)


def run_cmd(update, context):
    """Run user command."""
    global child
    if child is None:
        update.message.reply_text("Backdoor session expired, create new session. /new_session")
        return
    cmd = update.message.text
    child.sendline(cmd)
    child.expect('\$')
    output = child.before.decode() + child.after.decode()
    output = output.replace(cmd, "")
    for msg in [output[i:i+4096] for i in range(0, len(output), 4096)]:
        update.message.reply_text(msg)


def end_session(update, context):
    global child
    if child:
        child.kill(0)
        update.message.reply_text("Backdoor session closed.")
    else:
        update.message.reply_text("Backdoor session already closed.")


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("new_session", new_session))
    dispatcher.add_handler(CommandHandler("end_session", end_session))

    # on noncommand i.e message - run commands
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, run_cmd))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    child = None
    main()
