from bot import bot

if __name__ == '__main__':
    bot.polling(none_stop=True)

# webhook
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
import telebot
import os
from flask import Flask, request
from bot import bot

import config, utils

server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    #bot.set_webhook(url="https://eec22663.ngrok.io/bot")
    return "!", 200


@server.route("/created", methods = ['POST'])
def price_list():
	utils.generate_price_list(config.wcapi)
	return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)
'''
