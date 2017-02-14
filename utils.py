#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlsxwriter
import telebot
from database import User, Item, db

def create_order(message, wcapi, user, items):

	line_items = []
	for item in items:
		line_items.append({
			'product_id': item.product_id,
			'quantity': item.quantity
		})

	order = {
		"payment_method": "cod",
		"payment_method_title": u"Наложенный платёж",
		"set_paid": True,
		"billing": {
			"first_name": message.from_user.first_name,
			"last_name": message.from_user.last_name,
			"address_1": "",
			"address_2": "",
			"city": "",
			"state": "",
			"postcode": "702100",
			"country": "UZ",
			"email": user.email,
			"phone": user.phone
		},
		"shipping": {
			"first_name": message.from_user.first_name,
			"last_name": message.from_user.last_name,
			"address_1": "",
			"address_2": "",
			"city": "",
			"state": "",
			"postcode": "702100",
			"country": "UZ"
		},
		"line_items": line_items,
		"shipping_lines": [
			{
				"method_id": "free_shipping",
				"method_title": u"Бесплатная доставка",
				"total": 10
			}
		]
	}
	db.close()
	wcapi.post("orders", order)





def check_card(user):
	items = Item.select().where(Item.user_id == user.id)

	return items


def generate_price_list(wcapi):
	products = wcapi.get("products").json()
	workbook = xlsxwriter.Workbook("Price-List.xlsx")
	worksheet = workbook.add_worksheet("Price List - ultrashop.uz")

	header_format = workbook.add_format({
		'bold': 1, 
		'font_size': 14, 
		'bg_color': '#CFDBC5',
		'border': 1,
		'text_wrap': True
	})
	cell_format = workbook.add_format({
		'font_name': 'Times New Roman',
		'font_size': 13,
		'align': 'center',
		'border': 3,

	})
	# Set first column width to 50
	worksheet.set_column(0, 0, 50)
	# Set other columns width to 30
	worksheet.set_column(1, 11, 30)
	
	worksheet.write('A1', u'Продукт', header_format)
	worksheet.write('B1', u'Цена', header_format)
	worksheet.write('C1', u'ОЗУ (RAM)', header_format)
	worksheet.write('D1', u'CPU / Процессор', header_format)
	worksheet.write('E1', u'Видеокарта', header_format)
	worksheet.write('F1', u'Место хранения', header_format)
	worksheet.write('G1', u'Операционная система', header_format)
	worksheet.write('H1', u'Сеть / Технология подключения', header_format)
	worksheet.write('I1', u'Интерфейс', header_format)
	worksheet.write('J1', u'Дисплей экрана / Дизайн / Разрешение', header_format)
	worksheet.write('K1', u'Оптический привод', header_format)
	worksheet.write('L1', u'Слот памяти', header_format)
	worksheet.write('M1', u'Камера', header_format)

	index = 1
	for attr in  products[0]['attributes']:
		print attr
		print attr['options'][0].encode('utf-8')
	for product in products:
		worksheet.write(index, 0, product['name'], cell_format)
		worksheet.write(index, 1, product['price'], cell_format)
		
		ram = get_attr(product, 'Память(RAM)')
		cpu_processor = get_attr(product, 'CPU / Процессор')
		graphic_card = get_attr(product, 'Видеокарта')
		storage = get_attr(product, 'Место хранения')
		operating_system = get_attr(product, 'Операционная система')
		network = get_attr(product, 'Сеть / Технология подключения')
		interface = get_attr(product, 'Интерфейс')
		display = get_attr(product, 'Дисплей экрана / Дизайн / Разрешение')
		optical_drive = get_attr(product, 'Оптический привод')
		memory_slot = get_attr(product, 'Слот памяти')
		camera = get_attr(product, 'Камера')
		
		worksheet.write(index, 2, ram, cell_format)
		worksheet.write(index, 3, cpu_processor, cell_format)
		worksheet.write(index, 4, graphic_card, cell_format)
		worksheet.write(index, 5, storage, cell_format)
		worksheet.write(index, 6, operating_system, cell_format)
		worksheet.write(index, 7, network, cell_format)
		worksheet.write(index, 8, interface, cell_format)
		worksheet.write(index, 9, display, cell_format)
		worksheet.write(index, 10, optical_drive, cell_format)
		worksheet.write(index, 11, memory_slot, cell_format)
		worksheet.write(index, 12, camera, cell_format)
		print "RAM: ", ram

		index += 1
	
	workbook.close()



def get_attr(product, attr_name):
	attr = filter(lambda attr: attr['name'] == attr_name.decode('utf-8'), product['attributes'])
	if attr:
		return attr[0]['options'][0]
	
	return None



def send_products(bot, message, products):
	msg = None
	for product in products:
		#bot.send_photo(message.chat.id, product['images'][0]['src'])
		text = u"<b>{name} - {price}$</b>\n<b>CPU / Процессор</b> - {processor}\n<b>Память(RAM)</b> - {memory_ram}\n<b>Видеокарта</b> - {graphic_card}".format(
			name = product['name'],
			price = product['price'],
			processor = get_attr(product, "CPU / Процессор"),
			memory_ram = get_attr(product, "Память(RAM)"),
			graphic_card = get_attr(product, "Видеокарта")
		)
		keyboard = telebot.types.InlineKeyboardMarkup()
		add_button = telebot.types.InlineKeyboardButton(text = "\xF0\x9F\x92\xB3 Добавить в корзину", callback_data = str(product['id']))
		keyboard.add(add_button)			
		msg = bot.send_message(message.chat.id, text = text, parse_mode = 'HTML', reply_markup = keyboard)

	return msg

