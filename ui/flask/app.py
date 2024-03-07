from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from db import Query
import json

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)

# Get message by ts
class Message(Resource):
    def get(self, ts):
        res = Query(get='message',params={'ts':ts})
        return res.getData()

# Get channel list
class Channels(Resource):
    def get(self):
        res = Query(get='channels',params={})
        return res.getData()

# Get messages from channel
class Chat(Resource):
    def get(self, channel, limit, offset):
        res = Query(get='chat',params={'channel': channel,'limit': limit, 'offset': offset})
        return res.getData()

# Get replies
class Replies(Resource):
    def get(self, ts):
        res = Query(get='replies',params={'thread_ts': ts})
        return res.getData()

# Get messages from channel
class Search(Resource):
    def get(self, text, limit, offset):
        res = Query(get='search',params={'text': text, 'limit': limit, 'offset': offset})
        return res.getData()

api.add_resource(Message, '/message/<string:ts>')
api.add_resource(Channels, '/channels')
api.add_resource(Chat, '/chat/<string:channel>/<int:limit>/<int:offset>')
api.add_resource(Replies, '/replies/<string:ts>')
api.add_resource(Search, '/search/<string:text>/<int:limit>/<int:offset>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)

