import requests, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
'''

    Slack API v0.1
    -----------------------------------
    author:     Adam Mateusz Brożyński
    date:       2023-03-06
    license:    MIT

'''
class SlackApi:
    

    def __init__(self,server,token,cookie):
        self.server = server
        self.token  = token
        self.cookie = cookie
        self.limit  = 25

    # Get user data
    def user(self,user):
        fields={
                'user':         f'{user}',
                '_x_reason':    'with-call-menu'              
            }
        json = self.request(self.url('users.profile.get'),fields)
        # If no user return None
        if 'profile' not in json.keys(): return None
        profile = json['profile']
        # Return basic user data
        return {
            'user_name':profile['display_name'],
            'avatar':   profile['image_512'],
            'email':    profile['email']
            }

    # Get messages
    def messages(self,ts,channel,type='history',time='oldest',limit='50'):
        fields = {
            'channel':                          f'{channel}',
            'ts':                               f'{ts}',
            'limit':                            f'{limit}',
            'ignore_replies':                   'false',
            'include_free_team_extra_messages': 'true',
            'no_user_profile':                  'false',
            'include_stories':                  'true',
            'inclusive':                        'true',
            'include_pin_count':                'true',
            '_x_reason':                        'requestOfflineHistory'              
        }
        # check query type
        if time == 'oldest': fields['oldest'] = f'{ts}'
        else: fields['latest'] = f'{ts}'
        json = self.request(self.url('conversations.'+ type),fields)
        # If no messages return None
        if 'messages' not in json.keys(): return None
        return json['messages']

    # Get team id
    def team_id(self):
        default_channel = self.channel()
        if default_channel is None: return False 
        # Return team_id from default channel
        else: return default_channel['context_team_id']

    # Get channel name or first channel
    def channel(self,channel=None):
        fields={
                'canonical_avatars':            'false',
                'no_user_profile':              'true',
                'ignore_replies':               'true',
                'no_self':                      'true',
                'include_full_users':           'false',
                'include_use_case':             'false',
                'include_stories':              'false',
                'no_members':                   'true',
                'include_mutation_timestamps':  'false',
                'count':                        '28',
                'include_free_team_extra_messages': 'true',
            }
        # If channel is not given if will fetch default channel for server
        if channel: fields['channel'] = channel
        json = self.request(self.url('conversations.view'),fields)
        # Return None if no channel found
        if 'channel' not in json.keys(): return None
        return json['channel']

    # Get channels id list
    def channels(self):
        fields={
                'thread_counts_by_channel':         'true',
                'org_wide_aware':                   'true',
                'include_file_channels':            'true',
                '_x_reason':                        'client-counts-api/fetchClientCounts',
            }
        json = self.request(self.url('client.counts'),fields)
        # Return None if channels not found
        if 'channels' not in json.keys(): return None
        channel_list = []
        for channel in json['channels']:
            channel_list.append(channel['id'])
        return channel_list

    # Get channel name
    def channel_name(self,id):
        channel = self.channel(id)
        if 'name' not in channel.keys(): return None
        else: return channel['name']
    
    # Prepare request URL
    def url(self,url):
        return f'{self.server}/api/{url}'


    # Universal request handler
    def request(self,url,fields):
        headers = {
            'authority':            f'{self.server}',
            'accept':               '*/*',
            'accept-language':      'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie':               f'{self.cookie}', 
            'origin':               'https://app.slack.com',
            'pragma':               'no-cache' ,
            'cache-control':        'no-cache',
            'sec-ch-ua':            '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile':     '?0',
            'sec-ch-ua-platform':   '"Linux"',
            'sec-fetch-dest':       'empty', 
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-site',
            'sec-gpc':              '1',
            'user-agent':           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        add = {
            'token':        f'{self.token}',
            '_x_mode':      'online',
            '_x_sonic':     'true',
            '_x_app_name':  'client',
        }
        fields = fields | add
        data = MultipartEncoder(fields)
        headers['Content-Type'] = data.content_type
        response = requests.post(url, data=data, headers=headers)
        # Check for errors
        if (response.status_code!=200): 
            print(Fore.RED + f'{response.status_code}: {response.text}' + Fore.RESET)
            # TODO: Put additional error handling here, for ex. send e-mail with info that cookie has expired
            exit()
        else:
            # Return json response
            return json.loads(response.text)



    
