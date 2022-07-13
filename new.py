from tokenize import group
from telethon import functions, types
from telethon.tl.types import ChannelParticipantsAdmins
from ast import pattern
from collections import UserDict
from shelve import DbfilenameShelf
import time 
from typing import Text
from telethon import TelegramClient, events #,Button
from telethon.tl.custom import Button
from datetime import timedelta
import logging
import asyncio
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.types import InputPeerChannel
from traitlets import Integer
from scrape_utils import scrape_function_bsc, scrape_function_eth

from pyrogram import Client

from utils import checkBSC, checkETH


# My telegram api
api_id = 1479963
api_hash = '5181c1dd5f7492e61197f02b6dc4b276'


token = '5533082287:AAGnJTdevs7i1SgnWG9JfnyRAZqm4Pfutzk'

client1 = TelegramClient("bot1", api_id, api_hash).start(bot_token=token)
app = Client("my_account", api_id=api_id, api_hash=api_hash)

my_id = None
def main():

    client1.start()
    client1.parse_mode = 'md'
    print("Userbot on!")
    client1.run_until_disconnected()

# [emoji](https://c.tenor.com/UTDOJkmcvSkAAAAj/bitcoin-crypto.gif)


DB_DICT = {}

@client1.on(events.NewMessage(pattern='/activate@dev'))
# @client1.on(events.NewMessage())
async def user_add1(event):
    if type(event.original_update.message.peer_id) != PeerUser:
        global DB_DICT
        admin = None
        chat_entity = await client1.get_entity(event.original_update.message.peer_id)
        print('hello')

        # user =  await client1.get_participants(chat_entity.title)
        # print(user)
        user_id = event.original_update.message.from_id.user_id
        if type(event.original_update.message.peer_id) == PeerChannel:
            async for user in client1.iter_participants(chat_entity, filter=ChannelParticipantsAdmins):
                if user.id == user_id:
                    admin = True       
        else:
            await app.start()
            chat_id = event.original_update.message.peer_id.chat_id
            administrators = await app.get_chat_member(-chat_id, user_id)
            await app.stop()
            if str(administrators.status) == "ChatMemberStatus.OWNER" or str(administrators.status) == "ChatMemberStatus.ADMINISTRATORS": 
                admin = True       
        if admin:
            print(52, user_id)
            DB_DICT[user_id] = {}
            DB_DICT[user_id]['chat_entity'] = chat_entity
            DB_DICT[user_id]['Stage'] = 1
            DB_DICT[user_id]['path'] = None
            await client1.send_message(chat_entity.id, f'''
Thank you for using BuddhaBuyContestBot! 

To activate your contest, an admin must click this link & chat with the bot here >>[@BuddhaBuyContestBot](http://t.me/dev6546541245bot?start=captcha)
''', )

@client1.on(events.NewMessage(pattern='/start'))
async def user_add1(event):
    global DB_DICT
    if type(event.original_update.message.peer_id) == PeerUser:# 
        user_id = event.original_update.message.peer_id.user_id
        if user_id in DB_DICT:
            keyboard = [
                [Button.inline("BSC", b"21")],
                [Button.inline("ETH", b"22")]
            ]
            await client1.send_message(user_id, f'What blockchain does your token use?', buttons=keyboard)            
            DB_DICT[user_id]['Stage'] = 2
        else:
            username = (await client1.get_entity(user_id)).username
            await client1.send_message(user_id, f'''

Hello {username}, welcome to the BuddhaBuyContestBot!

I make running buy contests for BSC or ETH projects <b><u>EASY!</u></b>

I’m only in my Beta mode, so I currently only offer a <i>Biggest Buy Contest</i>, featuring two timer modes. I will eventually offer a <i>Last Buy contest, Random Buy contest</i> & maybe a contest designed by <b><u>YOU!</b></u>

To use me for your contest, just follow these 4 simple steps. 

1️⃣ Add @BuddhaBuyContestBot to your group.
2️⃣ Type /activate@BuddhaBuyContestBot
3️⃣ Click the link to come back here to set up your contest.
4️⃣ Start your Contest! 🎉

If you have any problems, questions, or suggestions, join our support group: @BuddhaBuyContestBotChat

Also, if you enjoy this bot, feel free to check out our project @BuddhaCoinCares. This is only our first utility of our soon-to-be massive ecosystem!
''', parse_mode='html')
    return None

@client1.on(events.NewMessage(pattern='/add_adv'))
async def user_add1(event):
    global DB_DICT
    if type(event.original_update.message.peer_id) == PeerUser:
        a = await client1.get_entity(event.original_update.message.peer_id)
        if a.username == 'Devshah9' or a.username == 'CapoTheDev':
            print(str(event.original_update.message.message))
            DB_DICT['Adv'] = str(event.original_update.message.message).split('/add_adv ')[-1]
            print(DB_DICT['Adv'])
            
@client1.on(events.NewMessage(pattern='/remove_adv'))
async def user_add1(event):
    global DB_DICT
    if type(event.original_update.message.peer_id) == PeerUser:
        a = await client1.get_entity(event.original_update.message.peer_id)
        if a.username == 'Devshah9' or a.username == 'CapoTheDev':
            del DB_DICT['Adv']
            if 'Adv_path' in DB_DICT:
                del DB_DICT['Adv_path']


@client1.on(events.NewMessage(pattern='/embed_link'))
async def user_add1(event):
    global DB_DICT
    DB_DICT['Adv_path'] = str(event.original_update.message.message).split('/embed_link ')[-1]



            
async def send_mess(chat_id, msg, file):
    global DB_DICT
    link_preview = False
    if "Adv" in DB_DICT:
        msg = msg + """
—————————————
`{}`""".format(DB_DICT['Adv'])
    if "Adv_path" in DB_DICT:
        print(148)
        msg = str(msg).replace(':', f'[:]({DB_DICT["Adv_path"]})', 1)
        link_preview = True
    await client1.send_message(chat_id, msg, file = file, link_preview=link_preview  )


@client1.on(events.NewMessage())
async def user_add1(event):
    global DB_DICT
    if type(event.original_update.message.peer_id) == PeerUser:
        user_id = event.original_update.message.peer_id.user_id
        if user_id in DB_DICT:
            if DB_DICT[user_id]['Stage'] == 3 and '/add_adv' not in event.original_update.message.message :
                print(144, event.original_update)
                if event.original_update.message.photo:
                    print('File Name :' + str(event.original_update.message.file.name))
                    path = await client1.download_media(event.original_update.message.media)
                    print('File saved to', path)  # printed after download is done
                    DB_DICT[user_id]['path'] = path                    

                DB_DICT[user_id]['Token'] =  event.original_update.message.message                
                await client1.send_message(user_id, f'Please enter the contract address for your token.')
                print(DB_DICT)             
                DB_DICT[user_id]['Stage'] = 35
            elif DB_DICT[user_id]['Stage'] == 35 and '/add_adv' not in event.original_update.message.message  :
                DB_DICT[user_id]['Token address'] =  event.original_update.message.message                
                if DB_DICT[user_id]['Blockchain'] == "BSC":
                    if checkBSC(DB_DICT[user_id]['Token address']):
                        DB_DICT[user_id]['Stage'] = 4
                    else: 
                        await client1.send_message(user_id, f"We couldn't find token on this address. Please enter the contract address for your token.")
                        return None
                    
                elif DB_DICT[user_id]['Blockchain'] == "ETH":
                    if checkETH(DB_DICT[user_id]['Token address']):
                        DB_DICT[user_id]['Stage'] = 4
                    else: 
                        await client1.send_message(user_id, f"We couldn't find token on this address. Please enter the contract address for your token.")
                        return None
                await client1.send_message(user_id, '''
How long would you like to run this contest?

Type a number, then a M (mins) or H (hours).

Examples:
__45 minutes = 45 M
2 hours = 2 H__
''')
                DB_DICT[user_id]['Stage'] = 45
            elif DB_DICT[user_id]['Stage'] == 45 and '/add_adv' not in event.original_update.message.message  :
                msg = event.original_update.message.message
                if ' ' in msg:
                    Time, Time_ms = msg.split(' ')  
                else:
                    await client1.send_message(user_id, 'Please make sure you have space between time and unit. \nExample : \n**10 M** for 10 minutes \n**2 H** for 2 hour')


                print(str(Time).isdigit(), str(Time_ms).lower())
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
                    keyboard = [
                        [Button.inline("Straight time", b"51")],
                        [Button.inline("Restart time", b"52")]
                    ]
                    await client1.send_message(user_id, '''
Which timer mode would you like for your contest?

Straight Time - The timer does not reset when a new big buy is found.

Timer Reset - The timer will reset every time a new big buy is found.
''', buttons=keyboard)
                    
                else:
                    await client1.send_message(user_id, 'Please Type a number with **M** and **H** for minutes and hours. \n Example : \n\n  **10 M** for 10 minutes \n\n  **2 H** for 2 hour')
            elif DB_DICT[user_id]['Stage'] == 6 and '/add_adv' not in event.original_update.message.message  :
                    DB_DICT[user_id]['Prize'] = event.original_update.message.message
                    
                    await client1.send_message(user_id, '''
Here are examples of how the posts will look in chat 👇👇
''')
                    if DB_DICT[user_id]['Mode'] == 'Straight time':
                        msg = """
**{} Biggest Buy Contest Tracker**

`📣 A new Biggest Buy Contest has started! 📣`

__Details:__
**Time:** {} Minutes 
**Mode:** Straight Time (The timer doesn’t not reset)
**Prize:** {}

__Bot powered by @BuddhaCoinCares__""".format(DB_DICT[user_id]['Token'], DB_DICT[user_id]['Time'], DB_DICT[user_id]['Prize'])
                        await send_mess(user_id, msg, DB_DICT[user_id]['path'])
                        msg = """
**{} Biggest Buy Contest Tracker**

__📣 Reminder, there is an ongoing Biggest Buy Contest! 📣__

Current Biggest Buy: 
**Amount Spent:** __20 BNB__ ($561.65) 
**Tx Hash:** [0X865...654163](https://bscscan.com/)
**Contest Time Remaining:** 30 Minutes Left
**Prize:**: {}

__Bot powered by @BuddhaCoinCares__""".format(DB_DICT[user_id]['Token'], DB_DICT[user_id]['Prize'])
                        await send_mess(user_id, msg, DB_DICT[user_id]['path'])

                    elif DB_DICT[user_id]['Mode'] == 'Reset time':
                        msg = """
**{} Biggest Buy Contest Tracker**

`📣 A new Biggest Buy Contest has started! 📣`

__Details:__
**Time:** {} Minutes left
**Mode:** Timer Reset (the timer resets when a new biggest buy is found)
**Prize:** {}

__Bot powered by @BuddhaCoinCares__""".format(DB_DICT[user_id]['Token'], DB_DICT[user_id]['Time'], DB_DICT[user_id]['Prize'])
                        await send_mess(user_id, msg, DB_DICT[user_id]['path'])
                        msg = """
**{} Biggest Buy Contest Tracker**

`💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥`

New Biggest Buy:
**Amount Spent:** __20 BNB__ ($456.54)
**TX Hash:** [0x465..54511](https://bscscan.com/)
**Contest Time Remaining:** __30 Minutes Left__
**Prize:** __{}__

__Bot powered by @BuddhaCoinCares__""".format(DB_DICT[user_id]['Token'],  DB_DICT[user_id]['Prize'])
                        await send_mess(user_id, msg, DB_DICT[user_id]['path'])
                    msg = '''

**{} Biggest Buy Contest Tracker**

__ 🎉 Contest Winner!! 🎉__

Winner: 
**Amount Spent:** __20 BNB__ ($54.56)
**Tx Hash:** [0x5461...4561](https://bscscan.com/)
**Contest Time Remaining:** __0 Minutes Left__
**Prize:**: __{}__

__Contact your project’s owner for payout details.__

__Bot powered by @BuddhaCoinCares__'''.format(DB_DICT[user_id]['Token'],  DB_DICT[user_id]['Prize'])
                    await send_mess(user_id, msg, DB_DICT[user_id]['path'])

                    await client1.send_message(user_id, f'''
If everything looks good, your contest will start in 2 minutes! 

If not, type " /start " to reset everything.

__Thank you for using @BuddhaBuyContestBot__
''')
                    # await asyncio.sleep(120)
                    await find_big_buy(DB_DICT[user_id])



@client1.on(events.CallbackQuery)
async def callback_bot(event):
    global DB_DICT
    user_id = event.original_update.user_id
    print('user_id', user_id, DB_DICT[user_id]['Stage'])
    if user_id in DB_DICT and DB_DICT[user_id]['Stage'] == 2:
        if event.query.data == b'21':
            DB_DICT[user_id]['Blockchain'] = 'BSC'
            await client1.send_message(user_id, 'You have selected **BSC**')
        if event.query.data == b'22':
            DB_DICT[user_id]['Blockchain'] = 'ETH'
            await client1.send_message(user_id, 'You have selected **ETH**')
        DB_DICT[user_id]['Stage'] = 3
        await event.delete()
        await client1.send_message(user_id,'''
What is the name of your token.

__*Use proper capitalization as this will be
displayed at the top of every post.__''')


    if user_id in DB_DICT and DB_DICT[user_id]['Stage'] == 4:
        print(105, event)
        if event.query.data == b'41':
            DB_DICT[user_id]['Time'] = 15
            await client1.send_message(user_id, 'You have selected 15 mins')
        elif event.query.data == b'42':
            DB_DICT[user_id]['Time'] = 30
            await client1.send_message(user_id, 'You have selected 30 mins')
        elif event.query.data == b'43':
            DB_DICT[user_id]['Time'] = 45
            await client1.send_message(user_id, 'You have selected 45 mins')
        elif event.query.data == b'44':
            DB_DICT[user_id]['Time'] = 60
            await client1.send_message(user_id, 'You have selected 60 mins')
        DB_DICT[user_id]['Stage'] = 5
        await event.delete()
        keyboard = [
                    [Button.inline("Straight Time", b"51")],
                    [Button.inline("Timer Reset", b"52")]
                ]
        await client1.send_message(user_id, '''
Which timer mode would you like for your contest?

Straight Time - The timer does not reset when a new big buy is found.

Timer Reset - The timer will reset every time a new big buy is found.''', buttons=keyboard)
               
    elif user_id in DB_DICT and DB_DICT[user_id]['Stage'] == 5:
        if event.data == b'51':
            DB_DICT[user_id]['Mode'] = 'Straight time'
            await client1.send_message(user_id, 'You have selected Straight timer mode')

        elif event.data == b'52':
            DB_DICT[user_id]['Mode'] = 'Reset time'
            await client1.send_message(user_id, 'You have selected Reset timer mode')
        DB_DICT[user_id]['Stage'] = 6
        await event.delete()
        await client1.send_message(user_id, 'What will the prize be?')

        
async def find_big_buy(final_dict):
    print(final_dict)
    OLD_BUY = 0
    inital_time = int(final_dict['Time'])

    if final_dict['Mode'] == "Straight time":
        msg = """
**{} Biggest Buy Contest Tracker**

`📣 A new Biggest Buy Contest has started! 📣`

__Details:__
**Time:** {} Minutes 
**Mode:** Straight Time (The timer doesn’t not reset)
**Prize:** {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
    elif final_dict["Mode"] == "Reset time":
        msg = """
**{} Biggest Buy Contest Tracker**

`📣 A new Biggest Buy Contest has started! 📣`

__Details:__
**Time:** {} Minutes left
**Mode:** Timer Reset (the timer resets when a new biggest buy is found)
**Prize:** {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
    await send_mess(final_dict['chat_entity'], msg, final_dict['path'])
    await asyncio.sleep(60)
    while True:
        if final_dict['Mode'] == "Straight time":
            print(int(final_dict['Time']),' min left')
            if int(final_dict['Time']) > 0:
                if final_dict['Blockchain'] == "BSC":
                    scrape_info = scrape_function_bsc(final_dict['Token address'])
                elif final_dict['Blockchain'] == "ETH":
                    scrape_info = scrape_function_eth(final_dict['Token address'])
                if scrape_info is not None:
                    NEW_BUY, TRX_HASH, TRX_HASH_LINK, in_dollar = scrape_info
                    if OLD_BUY < NEW_BUY:
                        print(78, NEW_BUY)
                        OLD_BUY = NEW_BUY
                        msg = """
**{} Biggest Buy Contest Tracker**

`💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥`

New Biggest Buy:
**Amount Spent:** __{} BNB__ (${})
**TX Hash:** [{}..{}]({})
**Contest Time Remaining:** __{} Minutes Left__
**Prize:** __{}__

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:3], TRX_HASH[-3:-1], TRX_HASH_LINK,  final_dict['Time'],final_dict['Prize'])
                    
                    else:
                        msg = """
**{} Biggest Buy Contest Tracker**

__📣 Reminder, there is an ongoing Biggest Buy Contest! 📣__

Current Biggest Buy: 
**Amount Spent:** __{} BNB__ (${})
**Tx Hash:** [{}...{}]({})
**Contest Time Remaining:** {} Minutes Left
**Prize:**: {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:4], TRX_HASH[-3:-1], TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
                    await send_mess(final_dict['chat_entity'], msg, final_dict['path'])
                else:
                    msg = """
**{} Biggest Buy Contest Tracker**

__📣 Reminder, there is an ongoing Biggest Buy Contest! 📣__

**Contest Time Remaining:** {} Minutes Left
**Prize:**: {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
                await send_mess(final_dict['chat_entity'], msg, final_dict['path'])

                await asyncio.sleep(60)
                final_dict['Time'] = int(final_dict['Time']) - 5
            else:
                msg = """
**{} Biggest Buy Contest Tracker**

__ 🎉 Contest Winner!! 🎉__

Winner:
**Amount Spent:** __{} BNB__ (${}) 
**Tx Hash:** [{}...{}]({})
**Contest Time Remaining:** __0 Minutes Left__
**Prize:**: __{}__

__Contact your project’s owner for payout details.__

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:4], TRX_HASH[-3:-1], TRX_HASH_LINK, final_dict['Prize']) 
                await send_mess(final_dict['chat_entity'], msg, final_dict['path'])

                break
        if final_dict["Mode"] == "Reset time":
            print(int(final_dict['Time']))
            if int(final_dict['Time']) > 0:
                if final_dict['Blockchain'] == "BSC":
                    scrape_info = scrape_function_bsc(final_dict['Token address'])
                elif final_dict['Blockchain'] == "ETH":
                    scrape_info = scrape_function_eth(final_dict['Token address'])
                if scrape_info is not None:
                    NEW_BUY, TRX_HASH, in_dollar = scrape_info
                    if OLD_BUY < NEW_BUY:
                        print(95, NEW_BUY)
                        final_dict['Time'] = inital_time
                        msg = """  
**{} Biggest Buy Contest Tracker**

__💥 A NEW BIGGEST BUY HAS BEEN FOUND 💥__

New Biggest Buy: 
**Amount Spent:** {} BNB (${})
**TX Hash:** [{}..{}]({})
**Contest Time Remaining:** {} Minutes Left
**Prize:** {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:3], TRX_HASH[-3:-1], TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
                        await send_mess(final_dict['chat_entity'], msg, final_dict['path'])
                        OLD_BUY = NEW_BUY
                    else :
                        final_dict['Time'] = int(final_dict['Time']) - 5
                        msg = """
**{} Biggest Buy Contest Tracker**

__📣 Reminder, there is an ongoing Biggest Buy Contest! 📣__

Current Biggest Buy: 
**Amount Spent:** __{} BNB__ (${})
**Tx Hash:** [{}...{}]({})
**Contest Time Remaining:** {} Minutes Left
**Prize:**: {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:4], TRX_HASH[-3:-1], TRX_HASH_LINK, final_dict['Time'], final_dict['Prize'])
                        await send_mess(final_dict['chat_entity'], msg, final_dict['path'])
                else:
                    final_dict['Time'] = int(final_dict['Time']) - 5

                    msg = """
**{} Biggest Buy Contest Tracker**

__📣 Reminder, there is an ongoing Biggest Buy Contest! 📣__

**Contest Time Remaining:** {} Minutes Left
**Prize:**: {}

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], final_dict['Time'], final_dict['Prize'])
                await send_mess(final_dict['chat_entity'], msg, final_dict['path'])

                await asyncio.sleep(60)
            else:
                msg = """
**{} Biggest Buy Contest Tracker**

__ 🎉 Contest Winner!! 🎉__

Winner: 
**Amount Spent:** __{} BNB__ (${})
**Tx Hash:** [{}...{}]({})
**Contest Time Remaining:** __0 Minutes Left__
**Prize:**: __{}__

__Contact your project’s owner for payout details.__

__Bot powered by @BuddhaCoinCares__""".format(final_dict['Token'], NEW_BUY, in_dollar, TRX_HASH[0:4], TRX_HASH[-3:-1], TRX_HASH_LINK, final_dict['Prize']) 
                await send_mess(final_dict['chat_entity'], msg, final_dict['path'])

                break
                

    final_dict = None
    print('done')


if __name__ == '__main__':
    main()
