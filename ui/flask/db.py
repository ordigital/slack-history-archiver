import json, sqlite3 

class Query:
    
    # Get query dict
    def __init__(self, get, params):
        self.get = get
        self.params = params
        self.queries = {
            'message': 'SELECT * FROM chat WHERE ts = :ts',
            'channels': 'SELECT DISTINCT channel FROM chat ORDER BY channel ASC;',
            'chat': 'SELECT * FROM chat WHERE channel = :channel AND is_reply = 0 ORDER BY ts DESC LIMIT :limit OFFSET :offset',
            'replies': 'SELECT * FROM chat WHERE is_reply = 1 AND thread_ts = :thread_ts ORDER BY ts ASC;',
            'search': 'SELECT * FROM chat WHERE text LIKE "%" || :text || "%" ORDER BY ts DESC LIMIT :limit OFFSET :offset',
        }
    
    # Execute sql query
    def sqlQuery(self,query,params):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        res = cursor.execute(query,params)
        result = [dict(row) for row in res.fetchall()]
        conn.close()
        return result
    
    # Get items from database
    def getData(self):
        try:  
            result = self.sqlQuery(self.queries[self.get],self.params)

            # Check if result exist
            if result and result[0] is not None:
                if self.get == 'channels': result = [item["channel"] for item in result]
                if self.get == 'chat' or self.get == 'message': result = self.getReplies(result)
                return result
            else:
                return {}
        except sqlite3.OperationalError as e:
            return { 'error': f'SQL error: {e}'}

    # Unpack additional data from message
    def getReplies(self,result):
        for i, message in enumerate(result):
            # get replies
            params = {'thread_ts': message['ts']}
            result[i]["replies"] = self.sqlQuery(self.queries['replies'],params)
            for r, reply in enumerate(result[i]["replies"]):
                result[i]["replies"][r] = self.getAttachments(result[i]["replies"][r])
            result[i]["reply_count"] = len(result[i]["replies"])
            result[i] = self.getAttachments(result[i])

        return result

    # Unpack attachments
    def getAttachments(self,message):
        message["attachments"] = json.loads(message["attachments"])
        return message