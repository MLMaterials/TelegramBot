import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

updater = Updater(token='543173045:AAENr6NMX4I5in7QquEL-w7P6hF5xB15kDI')

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True) #This is required to let handler to know what it to pass the list of command arguments to the callback.
dispatcher.add_handler(caps_handler)

# inline mode
def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

# command filer to reply to all commands that were not recognized by the previous handlers
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# ^ This handler MUST be added last. If you added it sooner, it woulde be trigerred before the CommandHandlers had a chance to look at the update. Once an update is handled, all further handlers are ignored. To circumvent this, you can pass the keyword argument group(int) to add_handler with a value other than 0.


