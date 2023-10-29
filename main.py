import telebot
from telebot import types
from telebot.types import WebAppInfo, ShippingOption

bot = telebot.TeleBot("6961282310:AAEiGDvS0eFShH9YIxVUUq5yJgSObbDn9iw")
PAYMENTS_TOKEN = '401643678:TEST:0363ce47-d7c7-47d4-8491-170838062f73'
keyboard = WebAppInfo(url='https://heyartemno.github.io/testtelegramwebapp/')

PRICE = {
    '1': [types.LabeledPrice(label='Зефир', amount=100*100)],
    '2': [types.LabeledPrice(label='Маршмеллоу', amount=120*100)],
    '3': [types.LabeledPrice(label='Шоколадное печенье', amount=120*100)],
    '4': [types.LabeledPrice(label='Фисташковое печенье', amount=120*100)],
    '5': [types.LabeledPrice(label='Безе', amount=100*100)],
    '6': [types.LabeledPrice(label='Ириска', amount=120*100)]
}

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз'
).add_price(types.LabeledPrice('Самовывоз', 0))

RUSSIA_SHIPPING_OPTION = types.ShippingOption(
    id='russia',
    title='По России'
).add_price(types.LabeledPrice('Доставка по России', 500*100))

VOLGOGRAD_SHIPPING_OPTION = ShippingOption(id='volgograd',title='По Волгограду')
VOLGOGRAD_SHIPPING_OPTION.add_price(types.LabeledPrice('Доставка', 200*100))

@bot.message_handler(commands=['start'])
def start(message):
        mess = f"Привет, <b>{message.from_user.first_name}</b>👋 \n\nСамые вкусные сладости можно заказать по кнопке ниже😋👇"
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('Заказать', web_app=keyboard))
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types= ["web_app_data"])
def buy_process(web_app_message):
    bot.send_invoice(web_app_message.chat.id,
                     title='Корзина',
                     description='Самые вкусные сладости😋',
                     provider_token=PAYMENTS_TOKEN,
                     currency='rub',
                     need_name= True,
                     need_email=True,
                     need_phone_number=True,
                     is_flexible=True,
                     prices=PRICE[f'{web_app_message.web_app_data.data}'],
                     start_parameter='example',
                     invoice_payload='some_invoice')

@bot.pre_checkout_query_handler(lambda query: True)
def pre_checkout_process(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.shipping_query_handler(func=lambda query: True)
def process_shipping_query(shipping_query: types.ShippingQuery):
        print('shipping_query.shipping_address')
        print(shipping_query.shipping_address)

        if shipping_query.shipping_address.country_code != 'RU':
            return bot.answer_shipping_query(
                shipping_query.id,
                ok=False,
                error_message='К сожалению, мы пока не сможем выполнить доставку в эту страну😔 Но мы над этим работаем...'
            )

        shipping_options = [PICKUP_SHIPPING_OPTION]

        if shipping_query.shipping_address.country_code == 'RU':
            shipping_options.append(RUSSIA_SHIPPING_OPTION)

            if shipping_query.shipping_address.state == 'Волгоградская область':
                shipping_options.append(VOLGOGRAD_SHIPPING_OPTION)


        bot.answer_shipping_query(
            shipping_query.id,
            ok=True,
            shipping_options=shipping_options
        )

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: types.Message):
    bot.send_message(message.chat.id, 'Заказ оформлен')


bot.polling()