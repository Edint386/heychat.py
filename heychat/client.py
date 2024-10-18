import asyncio
from typing import Union

import aiohttp

from . import api
from ._types import MessageTypes
from .channel import PublicTextChannel, PublicVoiceChannel
from .gateway import Gateway


class Client:
    def __init__(self, token, gate):
        self.token = token
        self.base_url = 'https://chat.xiaoheihe.cn'
        self.session = None
        self.gate: Gateway = gate
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

    async def send(self, target: Union[PublicTextChannel, PublicVoiceChannel], content,
                   msg_type=MessageTypes.MD_WITH_MENTION):
        return (await target.send(content, msg_type))

    async def update_message(self, msg_id, content, room_id, channel_id,
                             msg_type=MessageTypes.MD_WITH_MENTION ,reply_id=None, **kwargs):
        data = {
            'msg_id': msg_id,
            'content': content,
            'room_id': room_id,
            'channel_id': channel_id,
            'msg_type': msg_type,
            **kwargs}
        if reply_id:
            data['reply_id'] = reply_id
        return await self.gate.exec_req(api.Message.update(**data))

    async def delete_message(self, msg_id, room_id, channel_id):
        return await self.gate.exec_req(api.Message.delete(msg_id, room_id, channel_id))

    async def upload(self, file):
        """
        :param file: file path or binary data
        """
        if isinstance(file, str):
            with open(file, 'rb') as f:
                res = await self.gate.exec_req(api.File.upload(f))
        else:
            res = await self.gate.exec_req(api.File.upload(file))
        return res['result']['url']

    async def requestor(self, method, endpoint, **kwargs):
        return await self.gate.request(method, endpoint, **kwargs)

    async def start(self):
        self.session = aiohttp.ClientSession()
        await asyncio.gather(self.gate.run())

