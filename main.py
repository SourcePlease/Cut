from config import TOKEN
from videoedit import *
import telebot as tb
import os
import uuid

bot = tb.TeleBot(TOKEN)

dialogues = {}

# Ensure directories exist
for i in ['InputFiles', 'OutputFiles']:
    if not os.path.exists(i):
        os.mkdir(i)

def savevideo(message, merge=False):
    video = message.video
    file_info = bot.get_file(video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = f"{message.from_user.id}.mp4" if not merge else f"{message.from_user.id}_{str(uuid.uuid4())[:8]}.mp4"
    filepath = os.path.join('InputFiles', filename)
    with open(filepath, 'wb') as file:
        file.write(downloaded_file)
    return filepath

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = tb.types.InlineKeyboardMarkup([[
        tb.types.InlineKeyboardButton('Cut ✂️', callback_data='Cut'),
        tb.types.InlineKeyboardButton('Speed Up ⏏️', callback_data='Speed'),
        tb.types.InlineKeyboardButton('Concatenate 🎞', callback_data='Concatenate')
    ]])
    bot.send_message(message.chat.id, '''Hello, I am a bot created for editing video files.
Choose an action''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'Continue':
        mergevideos(call.from_user.id)
        output_path = os.path.join('OutputFiles', f"{call.from_user.id}.mp4")
        bot.send_video(call.from_user.id, video=open(output_path, 'rb'))        
        for file_ in os.listdir('InputFiles/'):
            if str(call.from_user.id) in file_:
                os.unlink(os.path.join('InputFiles', file_))
        os.unlink(output_path)
    else:
        dialogues[call.from_user.id] = call.data
        bot.send_message(call.from_user.id, 'Send me your video')

@bot.message_handler(content_types=['video'])
def getuservideo(message):
    user_action = dialogues.get(message.from_user.id)
    if user_action:
        if user_action == 'Cut':
            savevideo(message)
            bot.send_message(message.chat.id, '''Okay, send me the timestamps in this format:
Start time:End time (If any of the timestamps are more than a minute, use seconds: 1 minute 30 seconds: 90)''')
        elif user_action == 'Speed':
            savevideo(message)
            bot.send_message(message.chat.id, '''By how much should I speed up the video? Send me a number in this format: Number''')
        elif user_action == 'Concatenate':
            savevideo(message, merge=True)
            keyboard = tb.types.InlineKeyboardMarkup([[
                tb.types.InlineKeyboardButton('Continue', callback_data='Continue')
            ]])
            bot.send_message(message.chat.id, 'Now just send me your videos for concatenation', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def getparams(message):
    user_action = dialogues.get(message.from_user.id)
    if user_action:
        try:
            if user_action == 'Cut':
                from_, to = tuple(map(int, message.text.split(':')))
                cropvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), startingtime=from_, endingtime=to, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Sending video...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
            elif user_action == 'Speed':
                speed = int(message.text)
                speedupvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), speed=speed, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Sending video...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
        
        input_path = os.path.join('InputFiles', f'{message.from_user.id}.mp4')
        output_path = os.path.join('OutputFiles', f'{message.from_user.id}.mp4')
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        del dialogues[message.from_user.id]

bot.polling()
