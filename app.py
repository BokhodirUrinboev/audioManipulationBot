##############################################################################################################
import os
import telebot
from telebot import types
from flask import Flask, request
import datetime
from pydub import AudioSegment
from audio import reverse_sound, speed_change, background_effect, text_to_speech
import re
from setings import API_TOKEN
###############################################################################################################
PATH_TEMP = "C:\\Users\\Bokhodir\\PycharmProjects\\audio_manipulation\data\\temp\\"
PATH_SOUND_EFFECT = "C:\\Users\\Bokhodir\\PycharmProjects\\audio_manipulation\data\\sound_effects\\"

app = Flask(__name__)
###############################################################################################################
bot = telebot.TeleBot(API_TOKEN)
###############################################################################################################
LANGUAGE_BUTTON_RU = "🇷🇺--Русcкий--🇷🇺"
LANGUAGE_BUTTON_EN = "🇬🇧--English--🇬🇧"
LANGUAGES = [LANGUAGE_BUTTON_RU, LANGUAGE_BUTTON_EN]
USERS = []
REVERSE_BUTTON = "--REVERSE AUDIO--"
SPEED_CHANGE_BUTTON = "--CHANGE SPEED OF AUDIO--"
BACKGROUND_EFFECT_BUTTON = "--ADD BACKGROUND ENVIRONMENT--"
TEXT_TO_SPEECH_BUTTON = "--TEXT TO SPEECH--"
SPEED = ["=x 0.1 =", "=x 0.2 =", "=x 0.3 =", "=x 0.4 =", "=x 0.5 =", "= x0.6 =", "=x 0.7 =", "=x 0.8 =", "=x 0.9 =", "=x 1.0 =", "=x 1.1 =", "=x 1.2 =", "=x 1.3 =",
          "=x 1.4 =", "=x 1.5 =", "=x 1.6 =", "=x 1.7 =", "=x 1.8 =", "=x 1.9 =", "=x 2.0 =", "=x 2.1 =", "=x 2.2 =", "=x 2.3 =", "=x 2.4 =", "=x 2.5 =", "=x 2.6 =", "=x 2.7 =", "=x 2.8 =", "=x 2.9 =", "= 3.0 ="]
SOUND_EFFECT = ["--AIRPORT--", "--NATURE--", "--RESTAURANT--"]
SOUND_E_N = {"--AIRPORT--":"airport.mp3", "--NATURE--":"nature.mp3", "--RESTAURANT--":"restaurant.mp3"}

###############################################################################################################
def get_sound_name(name):
    return SOUND_E_N.get(name)


def get_speed_number(name):
    numb = re.findall("\d+\.\d+",name)
    return float(numb[0])


@bot.message_handler(commands=['start'])
def start(message):
    global USERS
    chat_id = message.chat.id
    for i in USERS:
        if i['chat_id'] == chat_id:
            USERS.remove(i)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    markup.add(types.KeyboardButton(REVERSE_BUTTON))
    markup.add(types.KeyboardButton(SPEED_CHANGE_BUTTON))
    markup.add(types.KeyboardButton(BACKGROUND_EFFECT_BUTTON))
    markup.add(types.KeyboardButton(TEXT_TO_SPEECH_BUTTON))

    bot.send_message(chat_id=chat_id, text="--------CHOOSE FUNCTIONALITY --------", reply_markup=markup)

###############################################################################################


def button_checker_s_c(message):
    return message.text == SPEED_CHANGE_BUTTON


def button_checker_r(message):
    return message.text == REVERSE_BUTTON


def button_checker_b_e(message):
    return message.text == BACKGROUND_EFFECT_BUTTON


def button_checker_t_t_s(message):
    return message.text == TEXT_TO_SPEECH_BUTTON
##################################################################################################



##################################################################################################
####################################Reverse_Effect ###################################################


@bot.message_handler(func=button_checker_r)
def reverse_sound_msg(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    USER['chat_id'] = chat_id
    USERS.append(USER)
    msg = bot.send_message(chat_id=chat_id, text="----- SEND AUDIO -----")
    bot.register_next_step_handler(msg, reverse_sound_f)

def r_s_check(message):
    if message.content_type == 'voice':
        return True
    else:
        return False

@bot.message_handler(func=r_s_check)
def reverse_sound_f(message):
    global USERS
    msg = message.text
    lebel = message.from_user.first_name
    chat_id = message.chat.id
    if message.content_type == 'voice':
        USER = {}
        for i in USERS:
            if i['chat_id'] == chat_id:
                USER = i
                basename = PATH_TEMP+ "user_audio"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".ogg")
                audio_name = "_".join([basename, suffix])
                USER['audio_name'] = audio_name
        file_info = message.voice.file_id
        file = bot.get_file(file_info)
        downloaded_file = bot.download_file(file.file_path)

        with open(USER['audio_name'], 'wb') as new_file:
            new_file.write(downloaded_file)
        sound = AudioSegment.from_ogg(USER['audio_name'])
        sound_path, image_path = reverse_sound(sound, lebel + " GRAPH OF THE AUDIO")
        audio = open(sound_path, 'rb')
        bot.send_audio(chat_id, audio)
        photo = open(image_path, 'rb')
        bot.send_photo(USER['chat_id'], photo)

        for i in USERS:
            if i['chat_id'] == chat_id:
                USERS.remove(i)
        # os.remove(USER['photo_name'])
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.add(types.KeyboardButton(REVERSE_BUTTON))
        markup.add(types.KeyboardButton(SPEED_CHANGE_BUTTON))
        markup.add(types.KeyboardButton(BACKGROUND_EFFECT_BUTTON))
        markup.add(types.KeyboardButton(TEXT_TO_SPEECH_BUTTON))

        bot.send_message(chat_id=chat_id, text="--------CHOOSE FUNCTIONALITY --------", reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=chat_id, text="--- SEND ONLY AUDIO ---")
        bot.register_next_step_handler(msg, reverse_sound_f)


##################################################################################################
####################################Speed Change_Effect ###################################################


@bot.message_handler(func=button_checker_s_c)
def speed_change_f_msg(message):
    global USERS
    chat_id = message.chat.id
    msg = message.text
    USER = {}
    USER['chat_id'] = chat_id
    USERS.append(USER)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for i in SPEED:
        markup.add(types.KeyboardButton(i))
    msg = bot.send_message(chat_id=chat_id, text="----- CHOOSE SPEED -----", reply_markup=markup)
    bot.register_next_step_handler(msg, speed_choose)


def s_check(message):
    audio = message.text
    if audio in SPEED:
        return True
    else:
        return False



@bot.message_handler(func=s_check)
def speed_choose(message):
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    audio = message.text
    if audio in SPEED:
        USER['speed'] = audio
        msg = bot.send_message(chat_id=chat_id, text="----- SEND AUDIO -----")
        bot.register_next_step_handler(msg, speed_change_f)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        for i in SPEED:
            markup.add(types.KeyboardButton(i))
        msg = bot.send_message(chat_id=chat_id, text="----- PLEASE CHOOSE SPEED -----", reply_markup=markup)
        bot.register_next_step_handler(msg, speed_choose)


def s_ch_check(message):
    if message.content_type == 'voice':
        return True
    else:
        return False

@bot.message_handler(func=s_ch_check)
def speed_change_f(message):
    global USERS

    lebel = message.from_user.first_name
    chat_id = message.chat.id
    if message.content_type == 'voice':
        USER = {}
        for i in USERS:
            if i['chat_id'] == chat_id:
                USER = i
                basename = PATH_TEMP+ "user_audio"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".ogg")
                audio_name = "_".join([basename, suffix])
                USER['audio_name'] = audio_name
        file_info = message.voice.file_id
        file = bot.get_file(file_info)
        downloaded_file = bot.download_file(file.file_path)

        with open(USER['audio_name'], 'wb') as new_file:
            new_file.write(downloaded_file)
        sound = AudioSegment.from_ogg(USER['audio_name'])
        sound_path, image_path = speed_change(sound,get_speed_number(USER['speed']), lebel + " GRAPH OF AUDIO")
        audio = open(sound_path, 'rb')
        bot.send_audio(chat_id, audio)
        photo = open(image_path, 'rb')
        bot.send_photo(USER['chat_id'], photo)

        for i in USERS:
            if i['chat_id'] == chat_id:
                USERS.remove(i)
        # os.remove(USER['photo_name'])
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.add(types.KeyboardButton(REVERSE_BUTTON))
        markup.add(types.KeyboardButton(SPEED_CHANGE_BUTTON))
        markup.add(types.KeyboardButton(BACKGROUND_EFFECT_BUTTON))
        markup.add(types.KeyboardButton(TEXT_TO_SPEECH_BUTTON))

        bot.send_message(chat_id=chat_id, text="--------CHOOSE FUNCTIONALITY --------", reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=chat_id, text="--- SEND ONLY AUDIO ---")
        bot.register_next_step_handler(msg, speed_change_f)


####################################Backgound Effect ###################################################


@bot.message_handler(func=button_checker_b_e)
def background_effect_f_msg(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    USER['chat_id'] = chat_id
    USERS.append(USER)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for i in SOUND_EFFECT:
        markup.add(types.KeyboardButton(i))
    msg = bot.send_message(chat_id=chat_id, text="----- CHOOSE BACKGROUND SOUND -----", reply_markup=markup)
    bot.register_next_step_handler(msg, background_choose)


def b_check(message):
    audio = message.text
    if audio in SOUND_EFFECT:
        return True
    else:
        return False
@bot.message_handler(func=b_check)
def background_choose(message):
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i

    audio = message.text
    print(audio)
    if audio in SOUND_EFFECT:
        USER['background_audio'] = audio
        msg = bot.send_message(chat_id=chat_id, text="----- SEND AUDIO -----")
        bot.register_next_step_handler(msg, background_effect_f)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        for i in SOUND_EFFECT:
            markup.add(types.KeyboardButton(i))
        msg = bot.send_message(chat_id=chat_id, text="----- PLEASE SELECT THE AUDIO -----", reply_markup=markup)
        bot.register_next_step_handler(msg, background_choose)


def b_e_check(message):
    if message.content_type == 'voice':
        return True
    else:
        return False

@bot.message_handler(func=b_e_check)
def background_effect_f(message):
    global USERS
    msg  = message.text
    lebel = message.from_user.first_name
    chat_id = message.chat.id
    if message.content_type == 'voice':
        USER = {}
        for i in USERS:
            if i['chat_id'] == chat_id:
                USER = i
                basename = PATH_TEMP+ "user_audio"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".ogg")
                audio_name = "_".join([basename, suffix])
                USER['audio_name'] = audio_name
        file_info = message.voice.file_id
        file = bot.get_file(file_info)
        downloaded_file = bot.download_file(file.file_path)

        with open(USER['audio_name'], 'wb') as new_file:
            new_file.write(downloaded_file)
        sound = AudioSegment.from_ogg(USER['audio_name'])
        background = AudioSegment.from_mp3(PATH_SOUND_EFFECT+get_sound_name(USER['background_audio']))

        sound_path, image_path = background_effect(sound, background, 7, lebel)
        audio = open(sound_path, 'rb')
        bot.send_audio(chat_id, audio)
        photo = open(image_path, 'rb')
        bot.send_photo(USER['chat_id'], photo)

        for i in USERS:
            if i['chat_id'] == chat_id:
                USERS.remove(i)
        # os.remove(USER['photo_name'])
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.add(types.KeyboardButton(REVERSE_BUTTON))
        markup.add(types.KeyboardButton(SPEED_CHANGE_BUTTON))
        markup.add(types.KeyboardButton(BACKGROUND_EFFECT_BUTTON))
        markup.add(types.KeyboardButton(TEXT_TO_SPEECH_BUTTON))

        bot.send_message(chat_id=chat_id, text="--------CHOOSE FUNCTIONALITY --------", reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=chat_id, text="--- SEND ONLY AUDIO ---")
        bot.register_next_step_handler(msg, background_effect_f)



####################################TEXT TO SPEECH ###################################################


@bot.message_handler(func=button_checker_t_t_s)
def txt_to_speech_msg(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    USER['chat_id'] = chat_id
    USERS.append(USER)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RU))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_EN))
    msg = bot.send_message(chat_id=chat_id,
                           text="🇷🇺--Выберите язык--🇷🇺\n 🇬🇧--Choose language--🇬🇧",
                           reply_markup=markup)
    # msg = bot.send_message(chat_id=chat_id, text="----- SEND TEXT ONLY ENGLISH -----")
    bot.register_next_step_handler(msg, txt_to_speech_lang)


def lang_check(message):
    lang = message.text
    if lang in LANGUAGES:
        return True
    else:
        return False

@bot.message_handler(func=lang_check)
def txt_to_speech_lang(message):
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i

    lang = message.text
    if lang in LANGUAGES:
        txt = ""
        if (lang == LANGUAGE_BUTTON_EN):
            USER['lang'] = "en"
            txt = "----- SEND TEXT ONLY ENGLISH -----"
        else:
            USER['lang'] = "ru"
            txt = "----- ОТПРАВИТЬ ТЕКСТ ТОЛЬКО НА РУССКИЙ -----"
        msg = bot.send_message(chat_id=chat_id, text=txt)
        bot.register_next_step_handler(msg, txt_to_speech)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RU))
        markup.add(types.KeyboardButton(LANGUAGE_BUTTON_EN))
        msg = bot.send_message(chat_id=chat_id,
                               text="🇷🇺--Выберите язык--🇷🇺\n 🇬🇧--Choose language--🇬🇧",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, txt_to_speech_lang)

def t_t_s_check(message):
    if message.content_type == 'text':
        return True
    else:
        return False

@bot.message_handler(func=t_t_s_check)
def txt_to_speech(message):
    global USERS
    msg = message.text
    lebel = message.from_user.first_name
    chat_id = message.chat.id
    if message.content_type == 'text':
        USER = {}
        for i in USERS:
            if i['chat_id'] == chat_id:
                USER = i
                basename = PATH_TEMP+ "user_audio"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".ogg")
                audio_name = "_".join([basename, suffix])
                USER['audio_name'] = audio_name
        # file_info = message.voice.file_id
        # file = bot.get_file(file_info)
        # downloaded_file = bot.download_file(file.file_path)

        # with open(USER['audio_name'], 'wb') as new_file:
        #     new_file.write(downloaded_file)
        # sound = AudioSegment.from_ogg(USER['audio_name'])
        sound_path = text_to_speech(message.text, USER['lang'])
        audio = open(sound_path, 'rb')
        bot.send_audio(chat_id, audio)

        for i in USERS:
            if i['chat_id'] == chat_id:
                USERS.remove(i)
        # os.remove(USER['photo_name'])
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.add(types.KeyboardButton(REVERSE_BUTTON))
        markup.add(types.KeyboardButton(SPEED_CHANGE_BUTTON))
        markup.add(types.KeyboardButton(BACKGROUND_EFFECT_BUTTON))
        markup.add(types.KeyboardButton(TEXT_TO_SPEECH_BUTTON))

        bot.send_message(chat_id=chat_id, text="--------CHOOSE FUNCTIONALITY --------", reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=chat_id, text="--- SEND ONLY TEXT ---")
        bot.register_next_step_handler(msg, reverse_sound_f)


##################################################################################################

# bot.polling()

@app.route('/' + API_TOKEN , methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

#https://api.telegram.org/bot<868081058:AAFSj3Q2diNtIJnd0pt1xtC02HhhP06qxRs>/deleteWebhook?url=https://17f6244e.ngrok.io/
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://659f6bd9f4f5.ngrok.io/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)))
