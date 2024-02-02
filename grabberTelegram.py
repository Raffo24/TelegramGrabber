# telegram script that read message of many channels and save it in a sqlite db file
# 
# Author: Raffaele Ruggeri
# 
# Date: 2024-02-01
# 
# Version: 1.0
# 
# Usage: python3 telegram_channel.py <app_id> <api_hash>
#
# Description:
#   This script read messages from telegram channels and save it in a sqlite db file
#   It is possible to add channels to listen, update channels, delete all channels, delete all messages
#   It is possible to print all channels in db
#   It is possible to print all followed channels
#   It is possible to add a single channel

#   Usage:
#       LISTEN CHANNELS:
#           python3 grabberTelegram.py -l (or --listen) <app_id> <api_hash>
#       UPDATE CHANNELS:
#           python3 grabberTelegram.py -u (or --update) <channel_file_name>
#       ADD 1 CHANNEL:
#           python3 grabberTelegram.py --add-channel
#       PRINT all FOLLOWED CHANNELS:
#           python3 grabberTelegram.py --print-followed
#       PRINT all CHANNELS in DB:
#           python3 grabberTelegram.py --print-database
#       DELETE all CHANNELS from DB:
#           python3 grabberTelegram.py --delete-channels
#       DELETE all MESSAGES from DB:
#           python3 grabberTelegram.py --delete-messages
#       INSERT ID CANALI IN DB:
#           python3 grabberTelegram.py --add-ids <app_id> <api_hash>
#

import sqlite3
import sys
import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events, sync
def help(name):
    print(f'Usage: \
        \nLISTEN CHANNELS:\
        \n\tpython3 {name} -l (or --listen) <app_id> <api_hash>\
        \n UPDATE CHANNELS:\
        \n\tpython3 {name} -u (or --update) <channel_file_name>\
        \nADD 1 CHANNEL:\
        \n\tpython3 {name} --add-channel <app_id> <api_hash> \
        \nPRINT all FOLLOWED CHANNELS:\
        \n\tpython3 {name} --print-followed <app_id> <api_hash>\
        \n PRINT all CHANNELS in DB:\
        \n\tpython3 {name} --print-database\
        \nDELETE all CHANNELS from DB:\
        \n\t python3 {name} --delete-channels\
        \nDELETE all MESSAGES from DB:\
        \n\t python3 {name} --delete-messages\
        \nINSERT ID CANALI IN DB:\
        \n\t python3 {name} --add-ids <app_id> <api_hash>')

def add_channel(channel):
    try:
        c.execute("INSERT INTO channel (id_channel, name) VALUES (?,?)", (None, channel,))
        conn.commit()
    except:
        print("this channel already in the db: ", channel)
def update_channels(file):
    file = open(file, "r")
    if input("this will delete all channels in db, write 'YES' to continue: ") == "YES":
        c.execute("DELETE FROM channel")
        conn.commit()
        print("Updating channels...")
        for line in file:
            add_channel(line)
    else:
        print("Aborting...")
        sys.exit(1)
    
    file.close()
def initialize(id, hash):

    # create a telegram client
    client = TelegramClient('session_name', id, hash)
    client.start()
    # get all channels
    channels = client.get_dialogs()
    # get channels from db
    c.execute("SELECT name FROM channel")
    tmp = [item[0].strip() for item in c.fetchall()]
    # filter only channels and groups that are in db
    channels = [d for d in channels if (d.is_group or d.is_channel) and d.title.strip() in tmp]
    # filter channels
    return client, channels

def insert_id_canali(id, hash):
    client, channels = initialize(id, hash)
    for channel in channels:
        name = channel.title
        id = str(channel.id)
        c.execute("UPDATE channel SET id_channel = ? WHERE name = ?", (id, name))
    conn.commit()


def listen(id, hash):
    # initialize
    client, channels = initialize(id, hash)
    # check if there are channels to listen
    if len(channels) == 0:
        print("No channels to listen")
        sys.exit(1)
    #download messages history
    for channel in channels:
        print("Downloading messages from: ", channel.title)
        # no limit
        messages = client.get_messages(channel, limit=1000)
        for message in messages:
            date = message.date.strftime("%Y-%m-%d %H:%M:%S")
            message_id = message.id
            message = message.message
            try:
                c.execute("INSERT INTO telegram (date, message_id, channel, message) VALUES (?,?,?,?)", (date, message_id, channel.title, message))
            except:
                pass
        conn.commit()
    print("Downloaded messages from all channels")
    print(f'Channels to listen: {channels}\nListening...')
    channel = ""
    # read message from channels
    @client.on(events.NewMessage(chats=channels))
    async def my_event_handler(event):
        print(event.message)
        
        date = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
        if event.chat == None:
            if channel == "":
                channel = "Unknown"
        else:
            channel = event.chat.title
        if event.message != None:
            message_id = event.message.id
            message = event.message.message
            try:
                c.execute("INSERT INTO telegram (date, message_id, channel, message) VALUES (?,?,?,?)", (date, message_id, channel, message))
            except:
                pass
        conn.commit()

    client.run_until_disconnected()

def print_channels(id, hash):
    # create a telegram client
    client = TelegramClient('session_name', id, hash)
    client.start()
    # get all channels
    channels = client.get_dialogs()
    # filter only channels and groups that are in db
    channels = [d for d in channels if d.is_group or d.is_channel]
    for channel in channels:
        print(channel.title)

if __name__ == "__main__":
    # usage
    if len(sys.argv)  > 4 or len(sys.argv) == 1:
        help(sys.argv[0])
        sys.exit(1)

    # create a sqlite db file
    conn = sqlite3.connect('threat0x.db')
    c = conn.cursor()

    # create table telegram
    c.execute('''CREATE TABLE IF NOT EXISTS telegram (date text, message_id text, channel text, message text, PRIMARY KEY (message_id, channel))''')

    # create table channel
    c.execute('''CREATE TABLE IF NOT EXISTS channel (id_channel text, name text PRIMARY KEY)''')
                
    # ask for parameters app id and api hash
    if sys.argv[1] == "-l" or sys.argv[1] == "--listen":
        id = sys.argv[2]
        hash = sys.argv[3]
        listen(id, hash)
    elif sys.argv[1] == "--add-channel":
        add_channel(input("Insert channel name: "))
    elif sys.argv[1] == "--update" or sys.argv[1] == "-u":
        update_channels(sys.argv[2])
    elif sys.argv[1] == "--print-followed":
        id = sys.argv[2]
        hash = sys.argv[3]
        print_channels(id, hash)
    elif sys.argv[1] == "-print-database":
        c.execute("SELECT name FROM channel")
        for item in c.fetchall():
            print(item[0])
    elif sys.argv[1] == "--delete-channels":
        if input("this will delete all channels in db, write 'YES' to continue: ") == "YES":
            print ("Deleting channels...")
            c.execute("DROP TABLE channel")
            # create table channel
            c.execute('''CREATE TABLE IF NOT EXISTS channel (id_channel text, name text PRIMARY KEY)''')
            conn.commit()
        else:
            print("Aborting...")
            sys.exit(1)
    elif sys.argv[1] == "--delete-messages":
        if input("this will delete all messages in db, write 'YES' to continue: ") == "YES":
            print ("Deleting messages...")
            c.execute("DROP TABLE telegram")
            # create table telegram
            c.execute('''CREATE TABLE IF NOT EXISTS telegram (date text, message_id text, channel text, message text, PRIMARY KEY (message_id, channel))''')
            conn.commit()
        else:
            print("Aborting...")
            sys.exit(1) 
    elif sys.argv[1] == "--add-ids":
        id = sys.argv[2]
        hash = sys.argv[3]
        insert_id_canali(id, hash)
    else:
        help(sys.argv[0])
