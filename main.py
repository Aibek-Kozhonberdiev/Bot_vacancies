import telebot
import time
from telebot import types
from config import *
from vacancies import *

USER = []

bot = telebot.TeleBot(BOT_API)

kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.add(types.KeyboardButton('/help'))

def user(message):
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ''
    first_name = message.from_user.first_name if message.from_user.first_name is not None else ''
    id_ = message.from_user.id
    data = message.date
    text = message.text
    print(f'Name: {first_name, last_name}, id: {id_}, data: {time.ctime(data)}, text: {text}')
    if message.chat.id != ADMIN:
        USER.append(f'Name: {first_name, last_name}, id: {id_}, data: {time.ctime(data)}, text: {text}')

@bot.message_handler(commands=['start'])
def start_com(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJKvdkd1jXPppOIi88avVTmPEsDs55ZgAC3xIAAs0SyUsU05Pip6jvZy8E')
    bot.send_message(message.chat.id, text='Привет! Как я могу вам помочь?', reply_markup=kb)
    user(message)

@bot.message_handler(commands=['help'])
def play_bot(message):
    bot.send_message(
        message.chat.id, 
        '/start - Начать общение\n/help - Инструкция\n/vacancies - вакансии\n/bot - для администраторов'
    )
    user(message)

@bot.message_handler(commands=['vacancies'])
def vacancies_handler(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Найти вакансии', callback_data="btn1")
    btn3 = types.InlineKeyboardButton(text='Альтернативный заработок', url='https://dtf.ru/mobile/1282436-obzor-gachimuchi-become-dungeon-master')
    kb.add(btn1, btn3)
    bot.send_message(message.chat.id, 'Что интересует:', reply_markup=kb)
    user(message)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Обновить данные', callback_data="btn1")
    kb.add(btn1)
    if callback.data == "btn1":
        for i in main():
            bot.send_message(callback.message.chat.id, f"{i}")
        bot.send_message(callback.message.chat.id, '🌐', reply_markup=kb)

@bot.message_handler(commands=['bot'])
def bot_handler(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, f'{USER}')
    else:
        bot.send_message(message.chat.id, "Вы не админ")
        user(message)

bot.infinity_polling()
