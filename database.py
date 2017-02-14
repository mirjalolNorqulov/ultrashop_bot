from peewee import *

db = SqliteDatabase('data/ultrashop_bot_db.db')

class User(Model):
	first_name = CharField()
	last_name = CharField()
	address_1 = CharField(null = True)
	address_2 = CharField(null = True)
	email = CharField(null = True)
	phone = CharField(null = True)
	telegram_id = IntegerField()

	class Meta:
		database = db


class Item(Model):
	product_name = CharField()
	product_id = IntegerField()
	quantity = IntegerField()
	price = FloatField()
	user_id = ForeignKeyField(User, related_name = 'items')

	class Meta:
		database = db

