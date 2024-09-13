# client.py

import aiohttp

class Client:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://chat.xiaoheihe.cn'
        self.session = aiohttp.ClientSession()
        self.headers = {
            'Authorization': token,
            'token': token
        }
        self.params = {
            'client_type': 'heybox_chat',
            'x_client_type': 'web',
            'os_type': 'web',
            'x_os_type': 'bot',
            'x_app': 'heybox_chat',
            'chat_os_type': 'bot',
            'chat_version': '1.24.5'
        }

    async def send(self, target, content, type):
        url = f'{self.base_url}/chatroom/v2/channel_msg/send'
        data = {
            'channel_id': target.id,
            'msg': content,
            'msg_type': type,
            'room_id': target.guild_id
        }
        async with self.session.post(url, headers=self.headers, params=self.params, json=data) as resp:
            return await resp.json()

    async def upload(self, file_or_binary):
        url = 'https://chat-upload.xiaoheihe.cn/upload'
        data = aiohttp.FormData()
        if isinstance(file_or_binary, str):
            data.add_field('file', open(file_or_binary, 'rb'))
        else:
            data.add_field('file', file_or_binary)
        async with self.session.post(url, headers=self.headers, params=self.params, data=data) as resp:
            return await resp.json()
