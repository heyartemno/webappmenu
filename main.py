import telebot
from telebot import types
from telebot.types import WebAppInfo, ShippingOption
import gspread
from datetime import date

bot = telebot.TeleBot("6961282310:AAEiGDvS0eFShH9YIxVUUq5yJgSObbDn9iw")
PAYMENTS_TOKEN = '1832575495:TEST:c3800b2274e49496052d96246e70a767bb533cbbe4083799216cb2d37e6b3d3c'
keyboard = WebAppInfo(url='https://heyartemno.github.io/webappmenu/')
googlesheetl = 'https://docs.google.com/spreadsheets/d/1sdRZojd4lnGg94NSEiA-0Xbt8IJlLD-73N3KdhoEKR4/edit#gid=0'
gc = gspread.service_account(filename='webapp-403514-3a36d5522e92.json')
description = "Укажите дату доставки и дополнительные комментарии в поле ввода АДРЕС 2!"

PRICE = {
    '1_3': [types.LabeledPrice(label='Зефир (3шт)', amount=100 * 3 * 100)],
    '1_6': [types.LabeledPrice(label='Зефир (6шт)', amount=100 * 6 * 100)],
    '1_9': [types.LabeledPrice(label='Зефир (9шт)', amount=100 * 9 * 100)],
    '2': [types.LabeledPrice(label='Маршмеллоу', amount=120*100)],
    '3': [types.LabeledPrice(label='Шоколадное печенье', amount=120*100)],
    '4': [types.LabeledPrice(label='Фисташковое печенье', amount=120*100)],
    '5': [types.LabeledPrice(label='Безе', amount=100*100)],
    '6': [types.LabeledPrice(label='Ириска', amount=120*100)]
}
LABELS = {
    '1_3': 'Зефир (3шт)',
    '1_6': 'Зефир (6шт)',
    '1_9': 'Зефир (9шт)',
}

IMAGES = {
    '1_3': 'https://heyartemno.github.io/webappmenu/images/zefir.jpg',
    '1_6': 'https://heyartemno.github.io/webappmenu/images/zefir.jpg',
    '1_9': 'https://heyartemno.github.io/webappmenu/images/zefir.jpg',
}

ID = {
    'id_order': 1
}

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='0',
    title='Самовывоз'
).add_price(types.LabeledPrice('Самовывоз', 0))

RUSSIA_SHIPPING_OPTION = types.ShippingOption(
    id='500',
    title='По России'
).add_price(types.LabeledPrice('Доставка по России', 500*100))

VOLGOGRAD_SHIPPING_OPTION = ShippingOption(id='200', title='По Волгограду')
VOLGOGRAD_SHIPPING_OPTION.add_price(types.LabeledPrice('Доставка', 200*100))


@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, <b>{message.from_user.first_name}</b>👋 \n\nСамые вкусные сладости можно заказать по кнопке ниже😋👇"
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Заказать', web_app=keyboard))
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["web_app_data"])
def buy_process(web_app_message):
    ID['id_order'] += 1
    bot.send_invoice(web_app_message.chat.id,
                     title='Заказ №''{}'.format(ID['id_order']),
                     description=description,
                     provider_token=PAYMENTS_TOKEN,
                     currency='rub',
                     suggested_tip_amounts=[50*100, 100*100, 150*100],
                     max_tip_amount=150*100,
                     photo_url='{}'.format(IMAGES[f'{web_app_message.web_app_data.data}']),
                     photo_width=260,
                     photo_height=220,
                     need_name=True,
                     need_email=True,
                     need_phone_number=True,
                     is_flexible=True,
                     prices=PRICE[f'{web_app_message.web_app_data.data}'],
                     start_parameter='{}'.format(ID['id_order']),
                     invoice_payload='{}'.format(LABELS[f'{web_app_message.web_app_data.data}'])
                     )


@bot.pre_checkout_query_handler(lambda query: True)
def pre_checkout_process(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(pre_checkout_query)


@bot.shipping_query_handler(func=lambda query: True)
def process_shipping_query(shipping_query: types.ShippingQuery):
    if shipping_query.shipping_address.country_code != 'RU':
        return bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message="К сожалению, мы пока не сможем выполнить доставку в эту страну😔 Но мы над этим работаем..."
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
    id_order = ID['id_order']
    order = message.successful_payment.invoice_payload
    username = message.from_user.username
    name = message.successful_payment.order_info.name
    phone_number = message.successful_payment.order_info.phone_number
    email = message.successful_payment.order_info.email
    state = message.successful_payment.order_info.shipping_address.state
    city = message.successful_payment.order_info.shipping_address.city
    street_line1 = message.successful_payment.order_info.shipping_address.street_line1
    street_line2 = message.successful_payment.order_info.shipping_address.street_line2
    post_code = message.successful_payment.order_info.shipping_address.post_code
    summ = message.successful_payment.total_amount // 100
    today = date.today().strftime("%d.%m.%y")
    shipping = message.successful_payment.shipping_option_id

    sh = gc.open_by_url(googlesheetl)
    sh.sheet1.append_row(
        [today, id_order, username, name, phone_number, order, summ, email, shipping,
         state, city, street_line1, street_line2, post_code], table_range='A1')
    bot.send_message(message.chat.id,
                     f"<b>Заказ {ID['id_order']}</b> на сумму <b>{message.successful_payment.total_amount // 100}"
                     f" {message.successful_payment.currency}</b> оформлен", parse_mode='html')


@bot.message_handler(content_types=["text"])
def date_order(message: types.Message):
    mess_text = f"Для нового заказа воспользуйтесь кнопкой ниже☺️👇"
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Заказать', web_app=keyboard))
    bot.send_message(message.chat.id, mess_text, parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)
