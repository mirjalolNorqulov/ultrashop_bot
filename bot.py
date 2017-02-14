#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import re

import config
import markups
import utils
from config import wcapi
from database import User, Item, db

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(config.TOKEN)

def get_category(name):
    cats = filter(lambda cat: cat['name'] == name, markups.categories)
    if cats:
        return cats[0]
    return None


@bot.message_handler(commands=['start'])
def start(message):
    try:
        User.get(User.telegram_id == message.from_user.id)
        print "User exists!"
        db.close()
    except User.DoesNotExist:
        user = User(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            telegram_id=message.from_user.id)
        user.save()
        db.close()

    text = u"Добро пожаловать, " + message.from_user.first_name
    bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)

'''
@bot.message_handler(func=lambda message: message.text == markups.all_laptops_button.text)
def all_laptops(message):
    keyboard = ReplyKeyboardMarkup(row_width=1)
    keyboard.add(markups.next_button)
    keyboard.add(markups.back_button)
    text = "Ноутбуки от 1 до 5"
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    products = wcapi.get("products?page=1&per_page=5").json()
    msg = utils.send_products(bot, message, products)
    bot.register_next_step_handler(msg, lambda m: show_all_laptops(m, page=2))
    return


def show_all_laptops(message, page):
    query = "products?page={page}&per_page=5".format(page=page)

    products = wcapi.get(query).json()
    if not products:
        text = u"Вот и все ноутбуки, которые мы имеем"
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)
        return
    msg = utils.send_products(bot, message, products)
    bot.register_next_step_handler(msg, lambda m: show_all_laptops(m, page=page + 1))


@bot.message_handler(func=lambda message: message.text in markups.category_names)
def category_message(message):
    category = get_category(message.text)

    text = u"Вы выбрали {0}".format(message.text)
    msg = bot.send_message(message.chat.id, text=text, reply_markup=markups.category_markup)
    bot.register_next_step_handler(msg, lambda m: category_step(m, category))


def category_step(message, category):
    if message.text == markups.back_button.text.decode('utf-8'):
        text = u"Пожалуйста, выберите категорию"
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)

    elif message.text == markups.show_button.text:
        query = "products?category={0}&page={1}&per_page=5".format(category['id'], 1)
        products = wcapi.get(query).json()
        msg = None
        if products:
            text = u"<b>Продукты 1 - 5</b>"
            msg = bot.send_message(message.chat.id, text=text, reply_markup=markups.pagination_markup,
                                   parse_mode='HTML')
            msg = utils.send_products(bot, message, products)
            bot.register_next_step_handler(msg, lambda m: show_products(m, category, 2))
        else:
            text = "Продукты не найдены для этой категории"
            msg = bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)


def show_products(message, category, current_page):
    if message.text == markups.next_button.text:

        msg = None
        query = "products?category={0}&page={1}&per_page=5".format(category['id'], current_page)

        products = wcapi.get(query).json()
        if products:
            text = u"<b>Продукты {0} - {1}</b>".format((current_page - 1) * 5 + 1, current_page * 5)
            msg = bot.send_message(message.chat.id, text=text, parse_mode='HTML')
            msg = utils.send_products(bot, message, products)
            bot.register_next_step_handler(msg, lambda m: show_products(m, category, current_page + 1))
        else:
            text = u"Это все для этой категории"
            bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)

    elif message.text == markups.back_button.text.decode('utf-8'):
        text = u"Категория {name}".format(name=category['name'])

        msg = bot.send_message(message.chat.id, text=text, reply_markup=markups.category_markup)
        bot.register_next_step_handler(msg, lambda m: category_step(m, category))


@bot.message_handler(func=lambda message: message.text == markups.price_list_button.text.decode('utf-8'))
def price_list(message):
    price_list_doc = open("Price-List.xlsx", "rb")
    bot.send_document(message.chat.id, price_list_doc)


@bot.message_handler(func=lambda message: message.text == markups.show_card_button.text.decode('utf-8'))
def show_card(message):
    user = User.get(User.telegram_id == message.from_user.id)
    items = Item.select().where(Item.user_id == user.id)
    keyboard = ReplyKeyboardMarkup(row_width=1)
    keyboard.row(markups.back_button, markups.clear_button)
    keyboard.row(markups.checkout_button)
    msg = None
    if items:
        text = "<b>Ваша корзина</b>\n\n"
        sub_total = 0
        total = 0
        for item in items:
            text += "<b>{product_name}</b>\n".format(product_name=item.product_name)
            sub_total = item.quantity * item.price
            text += "{quantity}x{price}$={total}$\n\n".format(quantity=item.quantity, price=item.price, total=sub_total)
            total += sub_total

        text += "<b>Итого:</b> {total}$".format(total=total)
        msg = bot.send_message(message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
    else:
        msg = bot.send_message(message.chat.id, text="Ваша корзина пусто\nПожалуйста, выбирайте что нибудь")

    db.close()
    bot.register_next_step_handler(msg, card_step)


def card_step(message):
    if message.text == markups.back_button.text.decode('utf-8'):
        text = u"Пожалуйста, выберите категорию"
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)

    elif message.text == markups.clear_button.text.decode('utf-8'):
        user = User.get(telegram_id=message.from_user.id)
        query = Item.delete().where(Item.user_id == user.id)
        query.execute()
        bot.send_message(message.chat.id, text="Корзина была очищена\nПожалуйста, выберите категорию",
                         reply_markup=markups.root_markup)


@bot.message_handler(func=lambda message: message.text == markups.checkout_button.text.decode('utf-8'))
def checkout(message):
    user = User.get(User.telegram_id == message.from_user.id)
    items = Item.select().where(Item.user_id == user.id)
    db.close()
    if not items:
        text = "Ваша корзина пуста. Пожалуйста, выберите что-то"
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)
        return

    if not user.phone:
        text = "Пожалуйста, пришлите нам свой номер телефона для связи с вами.\n Нажмите на кнопку ниже \xE2\xAC\x87"
        keyboard = ReplyKeyboardMarkup()
        button = KeyboardButton(text="\xF0\x9F\x93\x9E Отправить мой номер", request_contact=True)
        keyboard.row(button)
        keyboard.row(markups.back_button)
        msg = bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, lambda m: phone_number_step(m, user, items))
        return

    utils.create_order(message, wcapi, user, items)
    text = "Благодарим Вас за Ваш выбор. Мы свяжемся с вами как можно скорее."
    bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)


def check_product_id(call):
    pattern = re.compile("^[0-9]+$")
    return pattern.match(call.data)


@bot.callback_query_handler(func=check_product_id)
def add_to_card(call):
    query = "products/{id}".format(id=call.data)
    product = wcapi.get(query).json()

    text = "Вы выбрали {name}\nВыберите количество или введите".format(name=product['name'])
    msg = bot.send_message(call.message.chat.id, text=text, reply_markup=markups.quantity_markup)

    bot.register_next_step_handler(msg, lambda m: quantity_step(m, product))


def quantity_step(message, product):
    pattern = re.compile("^[0-9]+$")

    quantity = pattern.match(message.text)

    if quantity:

        user = User.get(telegram_id=message.from_user.id)

        ## If item exists, just change the quantity
        try:
            item = Item.get(product_id=product['id'])
            item.quantity += int(quantity.group())
            item.save()
            db.close()
        except Item.DoesNotExist:
            item = Item(
                product_name=product['name'],
                product_id=product['id'],
                price=product['price'],
                quantity=quantity.group(),
                user_id=user.id
            )
            item.save()
            db.close()

        msg = bot.send_message(message.chat.id, text="Продукт добавлен в корзину", reply_markup=markups.root_markup)

    else:
        msg = bot.send_message(message.chat.id, text="Пожалуйста, введите допустимое количество.")
        bot.register_next_step_handler(msg, lambda m: quantity_step(m, product))


def phone_number_step(message, user, items):
    if message.text == markups.back_button.text.decode('utf-8'):
        text = "Пожалуйста, выберите категорию."
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)
        return

    if message.contact:
        user.phone = message.contact.phone_number
        user.save()
        db.close()
        utils.create_order(message, wcapi, user, items)

        text = "Благодарим Вас за Ваш выбор. Мы свяжемся с вами как можно скорее."
        bot.send_message(message.chat.id, text=text, reply_markup=markups.root_markup)
    else:
        text = "Пожалуйста, отправьте свой номер телефона, используя ниже кнопки"
        msg = bot.send_message(message.chat.id, text=text)
        bot.register_next_step_handler(msg, lambda m: phone_number_step(message, user, items))


'''
