# client.py

import aiohttp

class Client:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://chat.xiaoheihe.cn'
        self.session = aiohttp.ClientSession()
        self.headers = {
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
        await self.requestor('POST', 'send', json=data)

    async def upload(self, file):
        """
        :param file: file path or binary data
        """
        data = aiohttp.FormData()
        if isinstance(file, str):
            data.add_field('file', open(file, 'rb'))
        else:
            data.add_field('file', file)
        await self.requestor('POST', 'upload', data=data)

    async def requestor(self, method, endpoint, **kwargs):
        url = f'{self.base_url}/{endpoint}'
        async with self.session.request(method, url, headers=self.headers, params=self.params, **kwargs) as resp:
            responses = await resp.json()
        if responses.get("status") == "failed":
            raise Exception(responses.get('msg'))
        return responses
