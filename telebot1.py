import asyncio
import datetime
import json
import time
from multiprocessing import Pool

import telebot

bot = telebot.TeleBot("5781829484:AAE_S1ROChx2pQK5cnX8MwPEFb9O9-I43LM",parse_mode='markdown')

	
from apscheduler.schedulers.background import BackgroundScheduler
 
# Creates a default Background Scheduler
sched = BackgroundScheduler()

import time

from pyrogram import Client
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient, events  # ,Button
from telethon.tl.custom import Button
from telethon.tl.types import (ChannelParticipantsAdmins, PeerChannel,
                               PeerChat, PeerUser)

from scrape_utils import scrape_function_bsc, scrape_function_eth
from utils import checkBSC, checkETH

DB_DICT = {}

def background_fuction():
	global DB_DICT
	print(32, DB_DICT)
	for i in DB_DICT:
		if DB_DICT[i]['running'] == False and DB_DICT[i]['Stage'] == 7:
			find_big_buy(DB_DICT[i])


sched.add_job(background_fuction, 'interval',seconds=10,max_instances=100)

sched.start()
def send_mess(chat_id, msg, file):
	bot.send_message(chat_id, msg, disable_web_page_preview=True)


@bot.message_handler(regexp="/activate@buddha", chat_types=['group', 'supergroup'])
def activate_buddha(event):
	global DB_DICT
	admin = False
	from_user_id = event.from_user.id
	group_id = event.chat.id

	for i in bot.get_chat_administrators(group_id):
		if i.user.id == from_user_id:
			admin = True       
	if admin:
		DB_DICT[from_user_id] = {}
		DB_DICT[from_user_id]['Group ID'] = group_id
		DB_DICT[from_user_id]['Stage'] = 1
		DB_DICT[from_user_id]['path'] = None
		DB_DICT[from_user_id]['running'] = False
	bot.reply_to(event,  f'''
Thank you for using BuddhaBuyContestBot! 

To activate your contest, an admin must click this link & chat with the bot here >>[@BuddhaBuyContestBot](https://t.me/BuddhaBuyContestBot?start=captcha)
''', parse_mode = 'Markdown')


# @client1.on(events.NewMessage(pattern='/cancel'))
# async def user_add1(event):
#     global DB_DICT
#     user_id = event.original_update.message.peer_id.user_id
#     if user_id in DB_DICT:
#         del DB_DICT[user_id]
#         await client1.send_message(user_id, 'you contest has been canceled')



def Time_mode_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Straight Time", callback_data="CB_ST"),
				InlineKeyboardButton("Restart Time", callback_data="CB_RT"))
    return markup


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("BSC", callback_data="CB_BSC"),
				InlineKeyboardButton("ETH", callback_data="CB_ETH"))
    return markup

@bot.message_handler(commands=['start'], chat_types='private')
def start_command(event):
	print(84, event)
	global DB_DICT
	user_id = event.from_user.id
	if user_id in DB_DICT:
		bot.send_message(user_id, f'What blockchain does your token use?', reply_markup=gen_markup())            
		DB_DICT[user_id]['Stage'] = 2
	else:
		username = event.from_user.username
		if not username:
			username = event.from_user.first_name
			
		bot.send_message(user_id, f'''

Hello {username}, welcome to the BuddhaBuyContestBot\!

I make running buy contests for BSC or ETH projects __*EASY\!*__

I’m only in my Beta mode, so I currently only offer a _Biggest Buy Contest, featuring two timer modes\. I will eventually offer a Last Buy contest, Random Buy contest_ & maybe a contest designed by __*YOU\!*__

To use me for your contest, just follow these 4 simple steps\. 

1️⃣ Add @BuddhaBuyContestBot to your group\.
2️⃣ Type /activate@BuddhaBuyContestBot
3️⃣ Click the link to come back here to set up your contest\.
4️⃣ Start your Contest\! 🎉

If you have any problems, questions, or suggestions, join our support group: @BuddhaBuyContestBotChat

Also, if you enjoy this bot, feel free to check out our project @BuddhaCoinCares\. This is only our first utility of our soon\-to\-be massive ecosystem\!
''', parse_mode='MarkdownV2')

@bot.message_handler(chat_types='private', regexp='//*')
def add_adv_command(event):
	text = event.text
	print(116, text)
	if text.startswith('/'):
		global DB_DICT
		username = event.from_user.username
		if username == 'Devshah9' or username == 'CapoTheDev':
			if text.startswith('/add_adv '):
				DB_DICT['Adv'] = text.split('/add_adv ')[-1]
				print(DB_DICT['Adv'])
			if text.startswith('/remove_adv '):
				del DB_DICT['Adv']
			if text.startswith('/remove_link'):
				del DB_DICT['Adv_path']
			if text.startswith('/embed_link '):
				DB_DICT['Adv_path'] = text.split('/embed_link ')[-1]
            

@bot.message_handler()
def Contest_message_handler(event):
	global DB_DICT
	text = event.text
	user_id = event.from_user.id
	print(135, DB_DICT[user_id]['Stage'])
	if user_id in DB_DICT:
		if DB_DICT[user_id]['Stage'] == 3:
			DB_DICT[user_id]['Token'] =  text
			bot.send_message(user_id, 'Please enter the contract address for your token.')
			DB_DICT[user_id]['Stage'] = 35
		elif DB_DICT[user_id]['Stage'] == 35:
			DB_DICT[user_id]['Token address'] =  text           
			if DB_DICT[user_id]['Blockchain'] == "BSC":
				if checkBSC(DB_DICT[user_id]['Token address']):
					DB_DICT[user_id]['Stage'] = 4
				else: 
					bot.send_message(user_id, f"We couldn't find token on this address. Please enter the contract address for your token.")
					return None                    
			elif DB_DICT[user_id]['Blockchain'] == "ETH":
				if checkETH(DB_DICT[user_id]['Token address']):
					DB_DICT[user_id]['Stage'] = 4
				else: 
					bot.send_message(user_id, f"We couldn't find token on this address. Please enter the contract address for your token.")
					return None
			bot.send_message(user_id, '''
How long would you like to run this contest?

Type a number, then a M (mins) or H (hours).

Examples:
_45 minutes = 45 M
2 hours = 2 H_
''')
			DB_DICT[user_id]['Stage'] = 45
		elif DB_DICT[user_id]['Stage'] == 45:
			print(168)
			if ' ' in text:
				
				Time, Time_ms = text.split(' ')  
			else:
				print(172)
				bot.send_message(user_id, 'Please make sure you have space between time and unit. \nExample : \n*10 M* for 10 minutes \n*2 H* for 2 hour')
				print(100)
			if str(Time).isdigit() and str(Time_ms).lower() == 'm' or str(Time_ms).lower() == "h":
				if str(Time_ms).lower() == 'm':
					DB_DICT[user_id]['TIME_MS'] =  'Minutes'
				elif str(Time_ms).lower() == 'h':
					DB_DICT[user_id]['TIME_MS'] =  'Hour'
					Time = int(Time) * 60
				DB_DICT[user_id]['Time'] =  int(Time)
				print(127, DB_DICT[user_id]['Time'])
				DB_DICT[user_id]['Stage'] = 5
				print(DB_DICT)
				bot.send_message(user_id, '''
Which timer mode would you like for your contest?

Straight Time - The timer does not reset when a new big buy is found.

Timer Reset - The timer will reset every time a new big buy is found.
''', reply_markup=Time_mode_markup())

			else:
				bot.send_message(user_id, 'Please Type a number with *M* and *H* for minutes and hours. \n Example : \n\n  *10 M* for 10 minutes \n\n  *2 H* for 2 hour')
		elif DB_DICT[user_id]['Stage'] == 6:
			DB_DICT[user_id]['Prize'] = text

			bot.send_message(user_id, '''
Here are examples of how the posts will look in chat 👇👇
''')
			if DB_DICT[user_id]['Blockchain'] == 'BSC':
				UNIT = 'BNB'
				URL_LINK = 'https://bscscan.com/'
			if DB_DICT[user_id]['Blockchain'] == 'ETH':
				UNIT = 'ETH'
				URL_LINK = 'https://etherscan.io/'
			if DB_DICT[user_id]['Mode'] == 'Straight time':
				msg = """
*{} Biggest Buy Contest Tracker*

`📣 A new Biggest Buy Contest has started! 📣`

_Details:_
*Time:* {} Minutes 
*Mode:* Straight Time (The timer doesn’t not reset)
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(DB_DICT[user_id]['Token'], DB_DICT[user_id]['Time'], DB_DICT[user_id]['Prize'])
				send_mess(user_id, msg, DB_DICT[user_id]['path'])
				msg = """
*{} Biggest Buy Contest Tracker*

_📣 Reminder, there is an ongoing Biggest Buy Contest! 📣_

Current Biggest Buy: 
*Amount Spent:* _20 {}_ (~$561.65) 
*Tx Hash:* [0X865...654163]({})
*Contest Time Remaining:* 30 Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(DB_DICT[user_id]['Token'], UNIT, URL_LINK, DB_DICT[user_id]['Prize'])
				send_mess(user_id, msg, DB_DICT[user_id]['path'])

			elif DB_DICT[user_id]['Mode'] == 'Reset time':
				msg = """
*{} Biggest Buy Contest Tracker*

`📣 A new Biggest Buy Contest has started! 📣`

_Details:_
*Time:* {} Minutes left
*Mode:* Timer Reset (the timer resets when a new biggest buy is found)
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(DB_DICT[user_id]['Token'], DB_DICT[user_id]['Time'], DB_DICT[user_id]['Prize'])
				send_mess(user_id, msg, DB_DICT[user_id]['path'])
				msg = """
*{} Biggest Buy Contest Tracker*

`💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥`

New Biggest Buy:
*Amount Spent:* _20 {}_ (~$456.54)
*TX Hash:* [0x465..54511]({})
*Contest Time Remaining:* _30 Minutes Left_
*Prize:* _{}_

_Bot powered by @BuddhaCoinCares_""".format(DB_DICT[user_id]['Token'], UNIT, URL_LINK, DB_DICT[user_id]['Prize'])
				send_mess(user_id, msg, DB_DICT[user_id]['path'])
			msg = '''

*{} Biggest Buy Contest Tracker*

_ 🎉 Contest Winner!! 🎉_

Winner: 
*Amount Spent:* _20 {}_ (~$54.56)
*Tx Hash:* [0x5461...4561]({})
*Contest Time Remaining:* _0 Minutes Left_
*Prize:* _{}_

_Contact your project’s owner for payout details._

_Bot powered by @BuddhaCoinCares_'''.format(DB_DICT[user_id]['Token'], UNIT, URL_LINK, DB_DICT[user_id]['Prize'])
			send_mess(user_id, msg, DB_DICT[user_id]['path'])

			bot.send_message(user_id, f'''
If everything looks good, your contest will start in 2 minutes! 

If not, type " /start " to reset everything.

_Thank you for using @BuddhaBuyContestBot_
''')
			DB_DICT[user_id]['Stage'] = 7
				
				

                                                                              

@bot.callback_query_handler(func=lambda call: True)
def callback_bot(event):
	global DB_DICT
	user_id = event.from_user.id
	if user_id in DB_DICT and DB_DICT[user_id]['Stage'] == 2:
		if event.json['data'] == 'CB_BSC':
			DB_DICT[user_id]['Blockchain'] = 'BSC'
			bot.send_message(user_id, 'You have selected *BSC*')
		if event.json['data'] == 'CB_ETH':
			DB_DICT[user_id]['Blockchain'] = 'ETH'
			bot.send_message(user_id, 'You have selected *ETH*')
		DB_DICT[user_id]['Stage'] = 3
		bot.delete_message(event.message.chat.id, event.message.message_id)
		# TODO delete the message
        # await event.delete()
		print(user_id)
		bot.send_message(user_id,'''
What is the name of your token.

_*Use proper capitalization as this will be
displayed at the top of every post._''')
	elif user_id in DB_DICT and DB_DICT[user_id]['Stage'] == 5:
		
		if event.json['data'] == 'CB_ST':
			DB_DICT[user_id]['Mode'] = 'Straight time'
			bot.send_message(user_id, 'You have selected Straight timer mode')

		elif event.json['data'] == 'CB_RT':
			DB_DICT[user_id]['Mode'] = 'Reset time'
			bot.send_message(user_id, 'You have selected Reset timer mode')
		DB_DICT[user_id]['Stage'] = 6
		bot.delete_message(event.message.chat.id, event.message.message_id)
		# TODO delete the message
		# await event.delete()
		bot.send_message(user_id, 'What will the prize be?')


def find_big_buy(final_dict):
	global DB_DICT
	print(final_dict)
	final_dict['running'] = True
	OLD_BUY, in_dollar_old, not_new_buyed_min = 0, 0, 0
	UNIT = None
	inital_time = int(final_dict['Time'])

	if final_dict['Mode'] == "Straight time":
		msg = """
*{} Biggest Buy Contest Tracker*

`📣 A new Biggest Buy Contest has started! 📣`

_Details:_
*Time:* {} Minutes 
*Mode:* Straight Time (The timer doesn’t not reset)
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
	elif final_dict["Mode"] == "Reset time":
		msg = """
*{} Biggest Buy Contest Tracker*

`📣 A new Biggest Buy Contest has started! 📣`

_Details:_
*Time:* {} Minutes left
*Mode:* Timer Reset (the timer resets when a new biggest buy is found)
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
	send_mess(final_dict['Group ID'], msg, final_dict['path'])
	time.sleep(60)
	while True:
		contest_start = time.time()
		print(443, final_dict, DB_DICT)

		print('This is the current time', datetime.datetime.now().time())
		if final_dict['Mode'] == "Straight time":
			print(int(final_dict['Time']),' min left')
			if int(final_dict['Time']) > 0:
				if final_dict['Blockchain'] == "BSC":
					scrape_info = scrape_function_bsc(final_dict['Token address'])
					UNIT = 'BNB'
				elif final_dict['Blockchain'] == "ETH":
					UNIT = 'ETH'
					scrape_info = scrape_function_eth(final_dict['Token address'])
				if scrape_info is not None:
					NEW_BUY, TRX_HASH, NEW_TRX_HASH_LINK, in_dollar_new = scrape_info
					print(78, NEW_BUY, OLD_BUY, OLD_BUY < NEW_BUY)
					if OLD_BUY < NEW_BUY:
						not_new_buyed_min = 0
						OLD_BUY, in_dollar_old, OLD_TRX_HASH_LINK = NEW_BUY, in_dollar_new, NEW_TRX_HASH_LINK
						msg = """
*{} Biggest Buy Contest Tracker*

`💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥`

New Biggest Buy:
*Amount Spent:* _{} {}_ (~${})
*TX Hash:* [{}..{}]({})
*Contest Time Remaining:* _{} Minutes Left_
*Prize:* _{}_

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], NEW_BUY, UNIT, in_dollar_old, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK,  final_dict['Time'],final_dict['Prize'])
						send_mess(final_dict['Group ID'], msg, final_dict['path'])
					else:
						not_new_buyed_min += 1
				else:
					not_new_buyed_min +=1
				if not_new_buyed_min ==5 and final_dict['Time']!= 0:
					if OLD_BUY:
						msg = """
*{} Biggest Buy Contest Tracker*

_📣 Reminder, there is an ongoing Biggest Buy Contest! 📣_

_Current Biggest Buy:_
*Amount Spent:* _{} {}_ (~${}) 
*Tx Hash:* [{}...{}]({})
*Contest Time Remaining:* {} Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], OLD_BUY, UNIT, in_dollar_old, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
					else:
						msg = """
*{} Biggest Buy Contest Tracker*

_📣 Reminder, there is an ongoing Biggest Buy Contest! 📣_

*Contest Time Remaining:* {} Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
					send_mess(final_dict['Group ID'], msg, final_dict['path'])
					not_new_buyed_min = 0.
				print(426, time.time(), contest_start, (time.time() - contest_start) < 60)
				while (time.time() - contest_start) < 60:
					time.sleep(1)
					print(time.time() , contest_start)
				final_dict['Time'] = int(final_dict['Time']) - 1
			else:
				msg = """
*{} Biggest Buy Contest Tracker*

_ 🎉 Contest Winner!! 🎉_

Winner:
*Amount Spent:* _{} {}_ (~${}) 
*Tx Hash:* [{}...{}]({})
*Contest Time Remaining:* _0 Minutes Left_
*Prize:* _{}_

_Contact your project’s owner for payout details._

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], OLD_BUY, UNIT, in_dollar_old, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK, final_dict['Prize']) 
				send_mess(final_dict['Group ID'], msg, final_dict['path'])

				break
		if final_dict["Mode"] == "Reset time":
			print(int(final_dict['Time']), not_new_buyed_min)
			if int(final_dict['Time']) > 0:
				if final_dict['Blockchain'] == "BSC":
					UNIT = 'BNB'
					scrape_info = scrape_function_bsc(final_dict['Token address'])
				elif final_dict['Blockchain'] == "ETH":
					UNIT = 'ETH'
					scrape_info = scrape_function_eth(final_dict['Token address'])
				if scrape_info is not None:
					NEW_BUY, TRX_HASH, NEW_TRX_HASH_LINK, in_dollar_new = scrape_info
					print(498, NEW_BUY, OLD_BUY, OLD_BUY < NEW_BUY)
					if OLD_BUY < NEW_BUY:
						OLD_TRX_HASH_LINK = NEW_TRX_HASH_LINK
						not_new_buyed_min = 0
						final_dict['Time'] = inital_time
						msg = """  
*{} Biggest Buy Contest Tracker*

_💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥_

New Biggest Buy: 
*Amount Spent:* {} {} (~${})
*TX Hash:* [{}..{}]({})
*Contest Time Remaining:* {} Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], NEW_BUY, UNIT, in_dollar_new, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
						send_mess(final_dict['Group ID'], msg, final_dict['path'])
						OLD_BUY, in_dollar_old = NEW_BUY, in_dollar_new
					else :
						final_dict['Time'] = int(final_dict['Time']) - 1
						not_new_buyed_min += 1
				else:
					final_dict['Time'] = int(final_dict['Time']) - 1
					not_new_buyed_min += 1
				if not_new_buyed_min ==5 and final_dict['Time']!= 0:
					if OLD_BUY:
						msg = """
*{} Biggest Buy Contest Tracker*

_📣 Reminder, there is an ongoing Biggest Buy Contest! 📣_

_Current Biggest Buy:_
*Amount Spent:* _{} {}_ (~${}) 
*Tx Hash:* [{}...{}]({})
*Contest Time Remaining:* {} Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], OLD_BUY, UNIT, in_dollar_old, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
					else:
						msg = """
*{} Biggest Buy Contest Tracker*

_📣 Reminder, there is an ongoing Biggest Buy Contest! 📣_

*Contest Time Remaining:* {} Minutes Left
*Prize:* {}

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
					send_mess(final_dict['Group ID'], msg, final_dict['path'])
					not_new_buyed_min = 0
				while time.time() - contest_start < 60:
					time.sleep(1)
			else:
				# TODO
				# Add the logic that dont throw error if there is no new buy 
				#  Rn it showing error because of newbuy

				msg = """
*{} Biggest Buy Contest Tracker*

_ 🎉 Contest Winner!! 🎉_

Winner: 
*Amount Spent:* _{} {}_ (~${})
*Tx Hash:* [{}...{}]({})
*Contest Time Remaining:* _0 Minutes Left_
*Prize:* _{}_

_Contact your project’s owner for payout details._

_Bot powered by @BuddhaCoinCares_""".format(final_dict['Token'], OLD_BUY, UNIT, in_dollar_old, OLD_TRX_HASH_LINK.split('/')[-1][0:3], OLD_TRX_HASH_LINK.split('/')[-1][-4:-1], OLD_TRX_HASH_LINK, final_dict['Prize']) 
				send_mess(final_dict['Group ID'], msg, final_dict['path'])

				break
				

	final_dict = None
	print('done')








bot.infinity_polling()
