import telebot
from telebot import types
from telebot.types import WebAppInfo

bot = telebot.TeleBot("5175169529:AAG-6i3kXmnDyRUd2sjyqB5zDvWTs4DGbI4")

@bot.message_handler(commands=['start'])
def start(message):
        mess = f"Привет, <b>{message.from_user.first_name}</b>👋 \n\nСамые вкусные сладости можно заказать по кнопке ниже😋👇"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заказать', web_app=WebAppInfo(url='https://heyartemno.github.io/webappmenu/')))
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

bot.polling()