from storm.locals import *

class Channel(object):
    __storm_table__ = "channels"
    id      = Unicode(primary=True)
    name    = Unicode()
    team    = Unicode()
    
class Chat(object):
    __storm_table__ = "chat"
    ts          = Unicode(primary=True)
    team        = Unicode()
    channel     = Unicode()
    text        = Unicode()
    attachments = Unicode()
    user_name   = Unicode()
    avatar      = Unicode()
    email       = Unicode()
    is_reply    = Int()
    thread_ts   = Unicode()

def tables():
    return {
        "CREATE TABLE IF NOT EXISTS channels (id TEXT PRIMARY KEY,name TEXT, team TEXT);",
        "CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT,team TEXT,\
            channel TEXT, ts TEXT, text TEXT, attachments BLOB, user_name TEXT, avatar TEXT,\
            email TEXT, is_reply INTEGER, thread_ts TEXT)"
    }    
    