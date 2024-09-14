import asyncio

import aiohttp

from ._types import MessageTypes
from . import api

class Client:
    def __init__(self, token, gate):
        self.token = token
        self.base_url = 'https://chat.xiaoheihe.cn'
        self.session = aiohttp.ClientSession()
        self.gate = gate
        self.headers = {'token': token}
        self.params = {
            'client_type': 'heybox_chat',
            'x_client_type': 'web',
            'os_type': 'web',
            'x_os_type': 'bot',
            'x_app': 'heybox_chat',
            'chat_os_type': 'bot',
            'chat_version': '1.24.5'
        }

    async def send(self, target, content, msg_type=MessageTypes.MD_WITH_MENTION):
        return await self.gate.exec_req(api.Message.create(target.id, content, msg_type.value, target.guild_id))

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

    async def start(self):
        await asyncio.gather(self.gate.run())