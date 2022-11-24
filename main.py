import os
import json
import random

import requests
import telebot

from telebot import types



bot = telebot.TeleBot('5061926024:AAGJ_8lJglUq182j350ZZSdjnD4aOwX0kvE')
user_data = {
	'test': {
		'user_name': 'test',
		'name': 'admin1',
		'type': 'none',
		'answer': 'none',
		'point': 0
	},
	'1111111111': {
		'user_name': 'admin1',
		'name': 'Влад',
		'type': 'none',
		'answer': 'none',
		'point': 2
	},
	'2222222222': {
		'user_name': 'admin2',
		'name': 'Даша',
		'type': 'none',
		'answer': 'none',
		'point': 1
	},
	'3333333333': {
		'user_name': 'admin3',
		'name': 'Женя',
		'type': 'none',
		'answer': 'none',
		'point': 5
	}
}


# reading flags of europe
with open('evropa_countrys.json', 'r', encoding='utf-8') as f: 
	contry_e = json.load(f)

# reading flags of the world
with open('world_countrys.json', 'r', encoding='utf-8') as f: 
	contry_w = json.load(f)

# download flag pictures
def download_flag(url_flag, user_id):
	r = requests.get(url_flag)
	file_name = f"{user_id}_img.png"

	with open(file_name, 'wb') as f:
		f.write(r.content)

	return file_name

# send a picture of the flag
def send_message(bot, message, contry_list):
	global user_data

	count = int(random.uniform(0, len(contry_list)))
	file = download_flag(contry_list[count]['flag'], str(message.chat.id))
	title = contry_list[count]['title']

	buttons = [
			types.KeyboardButton(contry_list[int(random.uniform(0, len(contry_list)))]['title']), 
			types.KeyboardButton(contry_list[int(random.uniform(0, len(contry_list)))]['title']), 
			types.KeyboardButton(contry_list[int(random.uniform(0, len(contry_list)))]['title']), 
			title
		]

	random.shuffle(buttons)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(
			buttons[0], 
			buttons[1], 
			buttons[2], 
			buttons[3]
		)

	bot.send_photo(message.chat.id, photo=open(file, 'rb'), caption="Что это за страна?", reply_markup=markup)
	bot.send_message(message.chat.id, "Выбрать другую категорию - /start\nПосмотреть таблицу лидеров - /get_table", reply_markup=markup)

	user_data[str(message.chat.id)]['answer'] = title

	os.remove(file)

# command bot "start"
@bot.message_handler(commands=['start'])
def start(message):
	markup_inline = types.InlineKeyboardMarkup()

	item_one = types.InlineKeyboardButton(text='Европа', callback_data='e')
	item_two = types.InlineKeyboardButton(text='Все страны мира', callback_data='w')

	markup_inline.add(item_one, item_two)

	bot.send_message(message.chat.id, 'Бот создан для игры "Угадай страну по флагу"\n\nВыберите категорию', reply_markup=markup_inline)

	if str(message.chat.id) not in user_data:
		user_data[str(message.chat.id)] = {
			'user_name': message.from_user.username,
			'name': message.from_user.first_name,
			'type': 'e',
			'answer': 'none',
			'point': 0
		}

# command bot "get_table"
@bot.message_handler(commands=['get_table'])
def send_admin_user_data(message):
	first_lider = user_data['test']
	second_lider = user_data['test']
	third_lider = user_data['test']

	for user in user_data:
		if user_data[user]['point'] > first_lider['point']:
			first_lider = user_data[user]

	for user in user_data:
		if user_data[user]['point'] > second_lider['point'] and user_data[user]['point'] < first_lider['point']:
			second_lider = user_data[user]

	for user in user_data:
		if user_data[user]['point'] > third_lider['point'] and user_data[user]['point'] < first_lider['point'] and user_data[user]['point'] < second_lider['point']:
			third_lider = user_data[user]

	bot.send_message(message.chat.id,
					"*Таблица лидеров*\n\n" 
					f"🥇 {first_lider['user_name']}({first_lider['point']}) 🥇\n"
					f"🥈 {second_lider['user_name']}({second_lider['point']}) 🥈\n"
					f"🥉 {third_lider['user_name']}({third_lider['point']}) 🥉\n\n",
					parse_mode="Markdown",
				)

	bot.send_message(message.chat.id, "Выбрать категорию - /start\n")

# command bot "send_admin_user_data"
@bot.message_handler(commands=['send_admin_user_data'])
def send_admin_user_data(message):
	if str(message.chat.id) == '1829352344':
		for user in user_data:
			bot.send_message(message.chat.id, 
							f'ID - {user}\n'
							f'USER_NAME - {user_data[user]["user_name"]}\n'
							f'NAME - {user_data[user]["name"]}\n'
							f'POINT - {user_data[user]["point"]}\n'
							f'ANSWER - {user_data[user]["answer"]}\n'
							f'TYPE - {user_data[user]["type"]}\n'
						)
	else:
		markup_inline = types.InlineKeyboardMarkup()

		item_one = types.InlineKeyboardButton(text='Европа', callback_data='e')
		item_two = types.InlineKeyboardButton(text='Все страны мира', callback_data='w')

		markup_inline.add(item_one, item_two)

		bot.send_message(message.chat.id, 'Бот создан для игры "Угадай страну по флагу"\n\nВыберите категорию', reply_markup=markup_inline)

# category selection
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	global user_data

	if call.data == 'e':
		user_data[str(call.message.chat.id)]['type'] = 'e'

		send_message(bot, call.message, contry_e)

	elif call.data == 'w':
		user_data[str(call.message.chat.id)]['type'] = 'w'

		send_message(bot, call.message, contry_w)

# getting an answer
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if str(message.chat.id) not in user_data:
		user_data[str(message.chat.id)] = {
			'user_name': message.from_user.username,
			'name': message.from_user.first_name,
			'type': 'e',
			'answer': 'none',
			'point': 0
		}
	if message.text.lower() == user_data[str(message.chat.id)]['answer'].lower():
		user_data[str(message.chat.id)]["point"] += 1
		bot.send_message(message.chat.id, f'Верно\nКоличество ваших очков - {user_data[str(message.chat.id)]["point"]}')
	else:
		bot.send_message(message.chat.id, f'Не верно\n'
										f'Правильный ответ - {user_data[str(message.chat.id)]["answer"]}\n'
										f'Количество ваших очков - {user_data[str(message.chat.id)]["point"]}'
									)
	if user_data[str(message.chat.id)]['type'] == 'w':
		send_message(bot, message, contry_w)
	else:
		send_message(bot, message, contry_e)


# bot launch
if __name__ == '__main__':
	print('Bot processing')
	bot.infinity_polling()
