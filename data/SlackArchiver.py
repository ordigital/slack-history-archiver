#!/bin/env python3
import yaml, sqlite3, json, os
from datetime import datetime, timedelta
from requests_toolbelt.multipart.encoder import MultipartEncoder
from colorama import Fore, Style, Back
from storm.locals import *
from .SlackApi import SlackApi
from .SlackDatabase import Channel, Chat, tables
''' 
    
    name:    Slack History Archiver v0.1
    author:  Adam Mateusz Brożyński 
    date:    2024.03.6
    license: MIT
    
'''
class SlackArchiver:
    
    # Init
    def __init__(self):
        # Set working dir
        self.dir        = os.getcwd() + '/'
        # Set timestamps
        self.now        = datetime.now().timestamp()
        self.oldest     = (datetime.now() - timedelta(days=360)).timestamp()
        # Get config
        config          = self.getConfig()
        self.database   = self.dir + config['database']
        # Init api
        self.slack      = SlackApi(config['server'],config['token'],config['cookie'])
        # Init database
        self.db         = create_database('sqlite:'+config['database'])
        self.store      = Store(self.db)
        self.team       = self.slack.team_id()
        self.initDb()     
        # use self.doodoo() to start downloading data
    
    # Get config from slack_archive.yaml
    def getConfig(self):
        with open(self.dir + "config.yaml", "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    # Create db tables
    def initDb(self):
        for table in tables():
            self.store.execute(table)

    def saveMessage(self,channel,message,reply=0):
        if self.store.find(Chat, Chat.ts == message['ts']).one(): return None
        new = Chat()
        new.ts = message['ts']
        new.team = self.team
        new.channel = channel
        new.text = message['text']
        if 'attachments' not in message.keys(): message['attachments'] = '{}'
        new.attachments = json.dumps(message['attachments'])
        user = self.slack.user(user=message['user'])
        new.user_name = user['user_name']
        new.avatar = user['avatar']
        new.email = user['email']
        new.is_reply = reply
        if 'thread_ts' not in message.keys(): message['thread_ts'] = ''
        new.thread_ts = message['thread_ts']
        self.store.add(new)
        self.store.flush()
        return new
   
    # Get chat
    def getChat(self,channel,type='history',time='oldest'):
        channel_id = self.channels[channel]
        # set ts
        ts = self.store.find(Chat,Chat.channel==channel).max(Chat.ts)
        if not ts: ts = self.oldest
        # get messages
        messages = self.slack.messages(f'{ts}',channel_id,type,time)
        if not messages: return None    
        msg_count = len(messages)  
        real_date = datetime.fromtimestamp(float(ts)).date()
        print(Fore.BLUE + f'Fetched {msg_count} from "{channel}" with last date {real_date}.' + Fore.RESET)
        chat = []
        print(Back.BLUE + 'Processing messages…' + Back.RESET)
        # Processing
        i = 0
        for msg in messages:
            # Remove messages with "subtype" (channel_join etc.)
            if "subtype" not in msg:
                # Get and save replies
                if "reply_count" in msg.keys() and msg["reply_count"] > 0:
                    rts = msg['ts']
                    replies = self.slack.messages(channel=channel_id,ts=f'{rts}',type='replies',limit=1000,time=time)
                    del replies[0]
                    for r in replies:
                        self.saveMessage(message=r,channel=channel,reply=1)
                # Save message
                res = self.saveMessage(message=msg,channel=channel,reply=0)
                if res: i += 1
        if not i: return False
        print(Fore.BLUE + f'Processing complete.' + Fore.RESET)
        print(Back.YELLOW + f'Saving to database…' + Back.RESET)
        self.store.commit()
        return True  
    
    # Get channel info {'name': 'id', ...}
    def getChannels(self):
        # get channels id list
        channels_list = self.slack.channels()
        channels = {}
        # iterate and get names
        for channel in channels_list:
            if not self.store.find(Channel, Channel.id == channel).one():
                new         = Channel()
                new.id      = channel
                new.name    = self.slack.channel_name(channel)
                new.team    = self.team
                self.store.add(new)
                self.store.commit()
                print(f'Found and saved channel "{new.name}" ({new.id})')
        
        channels = self.store.find(Channel)
        self.channels = {str(ch.name): ch.id for ch in channels}     
            
    # Fetch all channels
    def doodoo(self):
        print(Back.BLUE + f'{self.slack.server} ({self.team})' + Back.RESET)     
        self.getChannels()
        ch_count = len(self.channels)
        print(Fore.BLUE + f'Using {ch_count} channels.' + Fore.RESET)     
        # Get last messages
        for channel in self.channels:
            self.chatLoop(channel,time='oldest')
            self.chatLoop(channel,time='latest')
            print(f'Channel "{channel}" is up to date.')
        print(Back.YELLOW + f'All done.' + Back.RESET )
        return True

    # loop 
    def chatLoop(self,channel,time):
        new = True
        i = 0
        while new == True:
            print(f'Fetching {time}…')
            new = self.getChat(channel=channel,time=time)

