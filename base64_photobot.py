import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import base64 
from urllib.request import urlopen

#create variable to hold file id of images uploaded to telegram server
fileID = None

#designate which bot by inserting relevant bot token
updater=Updater(token='',use_context=True)
dispatcher=updater.dispatcher

#function which is called when user sends /start
def start(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'hello, are you doing well? (Y/N)')

#message handler when bot recieves plain text
def greeting(update,context):
    if update.message.text == 'Y':
        context.bot.send_message(chat_id=update.effective_chat.id, text = "glad to hear" )
    elif update.message.text == 'N':
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Sad bois')
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "?")
    
#function which is called when user sends /send
#this function will send most recent image sent to bot back to user
def SendFile(update,context):
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo = fileID)

    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'sorry, no available photo')

#message handler when bot recieves image
def RecieveFile(update,context):
    global fileID
    #set file id to be the most recent image sent
    fileID = update.message.photo[-1].file_id
    #grab link of file and store in CurrentImage
    CurrentImage = context.bot.get_file(fileID)
    #open link and encode file in basae64
    EncodedImage = base64.b64encode(urlopen(CurrentImage.file_path).read()).decode('utf-8')
    
    '''
    CurrentImage.download('test.JPEG')
    
    with open('test.JPEG','rb') as imgFile:
        EncodedImage = base64.b64encode(imgFile.read())
    #print(EncodedImage.decode('utf-8'))
    '''
    #create text file and write encoded image text
    Base64_file = open('Base64.txt','w+')
    Base64_file.write(str(EncodedImage))
    Base64_file.close

    #send image back to user, currently send image found at link
    context.bot.send_photo(chat_id=update.effective_chat.id, photo= "https://cdna.artstation.com/p/assets/images/images/033/900/170/large/mickael-riciotti-highresscreenshot00000.jpg?1610871196")

#Make bot recognise /start and /send as commands
start_handler = CommandHandler('start',start)
send_handler = CommandHandler('send',SendFile)

#add handlers
#when message is recieved the handlers will be check top-down to see which handler must be used. 
#Only one handler can execute per condition.
dispatcher.add_handler(start_handler)
dispatcher.add_handler(MessageHandler(Filters.photo,RecieveFile))
dispatcher.add_handler(send_handler)
dispatcher.add_handler(MessageHandler(Filters.text,greeting))

#start bot
updater.start_polling()
#stops bot when stop signal is recieved, defaulted to SIGINT (ctrl+c)
updater.idle()
