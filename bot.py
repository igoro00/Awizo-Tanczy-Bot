import logging
import awizator
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater
from telegram import ChatAction
from datetime import datetime
from key import key

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Create key.py file and type "key = {YOUR KEY}"
updater = Updater(token=key, use_context=True) 
dispatcher = updater.dispatcher


logging.basicConfig(filename='logged_messages.log', format='%(asctime)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    update.message.reply_text("Wyślij plik dźwiękowy* a odeślę ci film jak awizo tańczy do tej piosenki.\n\n* Narazie obsługiwane tylko mp3. Jeśli audio jest dluższe od filmu(ok. 8s) to wykorzystane będzie tylko początek.")

def messageResponder(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
    audio_file = update.message.audio.get_file()
    audio_file.download("./files/"+update.message.audio.file_id+".mp3")
    context.bot.send_video(chat_id=update.effective_chat.id,
                            video=open(awizator.get_response_file("./files/"+update.message.audio.file_id+".mp3"), 'rb'),
                            reply_to_message_id = update.message.message_id)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
audio_handler = MessageHandler(Filters.audio, messageResponder)
dispatcher.add_handler(audio_handler)

updater.start_polling()
