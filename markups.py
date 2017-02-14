# -*- coding: utf-8 -*-
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import config

root_markup = ReplyKeyboardMarkup(row_width=4)

categories = config.wcapi.get("products/categories?parent=0").json()
category_names = [category['name'] for category in categories]

buttons = []
for category in categories:
    btn = KeyboardButton(text=category['name'])
    buttons.append(btn)


all_laptops_button = KeyboardButton(text=u"Все ноутбуки")
root_markup.row(all_laptops_button)
root_markup.add(*buttons)

show_card_button = KeyboardButton(text="\xF0\x9F\x93\xA5 Корзина")
checkout_button = KeyboardButton(text="\xF0\x9F\x93\xA4 Оформить заказ")
price_list_button = KeyboardButton(text="\xF0\x9F\x93\x9D Прайс-лист")
clear_button = KeyboardButton(text="\xF0\x9F\x94\x84 Очистить")

root_markup.row(show_card_button, checkout_button)
root_markup.row(price_list_button)
# -------------------------------------------------------------

category_markup = ReplyKeyboardMarkup(row_width=1)

show_button = KeyboardButton(text=u"Показать")
back_button = KeyboardButton("\xE2\xAC\x85 Назад")

category_markup.add(show_button, back_button)
# -------------------------------------------------------------

pagination_markup = ReplyKeyboardMarkup(row_width=1)

next_button = KeyboardButton(text=u"Следущая")

pagination_markup.add(next_button, back_button)

# -------------------------------------------------------------

quantity_markup = ReplyKeyboardMarkup(row_width=3)
buttons = []
for i in range(1, 10):
    btn = KeyboardButton(str(i))
    buttons.append(btn)

quantity_markup.add(*buttons)


#
