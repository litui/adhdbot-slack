"""Core library for bot operations.

Depends on the slacker library.
"""

import json
from cached_property import cached_property
from slacker import Slacker
from sql import session, Config
from websocket import WebSocketApp


class Bot(Slacker):
    def __init__(self):
        self.sql = session
        super().__init__(self.token)

        self._message_id = 0

    def get_channel_by_name(self, name):
        """Get channel from channel name.

        :param str name: Channel name (without '#')
        :returns: Channel object
        :rtype: dict
        """

        for channel in self.channel_list:
            if channel['name'] == name:
                return channel

        return {}

    def get_user_by_name(self, name):
        """Get user by user name.

        :param str name: User name
        :returns: User object
        :rtype: dict
        """

        for user in self.user_list:
            if user['name'] == name:
                return user

        return {}

    def run_rtm(self):
        """Run real-time-messaging with websocket.

        Starts rtm and immediately opens a websocket interface.
        """

        def on_message(ws, message):
            msg = json.loads(message)
            # Lock to only me at the moment to prevent spam.
            if msg.get('user') not in self.admin_user_ids:
                return

            if msg.get('type') == 'message':
                chan = msg.get('channel')
                if chan and chan[0] == 'C':
                    if chan in self.channel_id_attention:
                        print(msg.get('text'))
                elif chan and chan[0] == 'D':
                    if msg.get('text') == 'close_socket':
                        ws.send(json.dumps({
                            "id": self.msg_id,
                            "type": "message",
                            "reply_to": msg.get('id'),
                            "channel": chan,
                            "text": "Closing websocket..."
                        }))
                        ws.close()

            print(msg)

        response = self.rtm.start()
        ws_url = response.body['url']

        wsock = WebSocketApp(ws_url, on_message=on_message)
        wsock.run_forever()

    @cached_property
    def token(self):
        slack_token = self.sql.query(Config.value).\
            filter(Config.key == 'slack_token').first().value
        return slack_token

    @cached_property
    def channel_name_attention(self):
        channels = json.loads(
            self.sql.query(Config.value).filter(
                Config.key == 'channel_attention'
            ).first().value
        )
        return channels

    @cached_property
    def admin_users(self):
        users = json.loads(
            self.sql.query(Config.value).filter(
                Config.key == 'admin_users'
            ).first().value
        )
        return users

    @property
    def admin_user_ids(self):
        users = self.admin_users
        return [u['id'] for u in self.user_list if u['name'] in users]

    @property
    def channel_id_attention(self):
        return [c['id'] for c in self.channel_attention]

    @property
    def channel_attention(self):
        channels = self.channel_name_attention
        return [c for c in self.channel_list if c['name'] in channels]

    @property
    def msg_id(self):
        self._message_id += 1
        return self._message_id

    @cached_property
    def channel_list(self):
        response = self.channels.list()
        return response.body['channels']

    @cached_property
    def user_list(self):
        response = self.users.list()
        return response.body['members']
