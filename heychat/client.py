# client.py
import asyncio
import json
from typing import Union

import aiohttp


from . import api
from .guild import Guild
from ._types import MessageTypes, GuildRoleTypes
from .channel import PublicTextChannel, PublicVoiceChannel
from .gateway import Gateway
from .mdmessage import MDMessage


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

    # message related
    async def send(self, target: Union[PublicTextChannel, PublicVoiceChannel], content: Union[str, dict],
                   msg_type: MessageTypes = MessageTypes.MD_WITH_MENTION):

        return (await target.send(content, msg_type))

    async def update_message(self, msg_id, content, guild_id, channel_id,
                             msg_type=MessageTypes.MD_WITH_MENTION ,reply_id=None, **kwargs):
        data = {
            'msg_id': msg_id,
            'room_id': guild_id,
            'channel_id': channel_id,
            'msg_type': msg_type,
            **kwargs}
        if isinstance(content, MDMessage):
            data = {**data, **content.extra_info}
            content = str(content)
        elif isinstance(content, dict):
            data['msg_type'] = MessageTypes.CARD
            content = json.dumps(content)

        data['content'] = content

        if reply_id:
            data['reply_id'] = reply_id
        return await self.gate.exec_req(api.Message.update(**data))

    async def delete_message(self, msg_id, room_id, channel_id):
        return await self.gate.exec_req(api.Message.delete(msg_id, room_id, channel_id))


    # channel related
    async def fetch_channel(self, guild_id, channel_id) -> PublicTextChannel:
        '''not implemented, return a dummy channel'''
        return PublicTextChannel({'channel_base_info': {'channel_id': channel_id},'room_base_info': {'room_id': guild_id}}, self.gate)

    async def kick_out_voice_channel_user(self, user_id: int, room_id: str, channel_id: str):
        """Kick out a user from voice channel."""
        return await self.gate.exec_req(api.Channel.kick_out(user_id, user_id, room_id, channel_id))

    async def move_user(self, origin_channel_id: str, user_ids: Union[int, list], room_id: str, target_channel_id: str):
        """Move users from one voice channel to another."""
        if isinstance(user_ids, int):
            user_ids = [user_ids]
        return await self.gate.exec_req(api.Channel.move_user(origin_channel_id, user_ids, room_id, target_channel_id))


    #guild related
    async def fetch_guild(self, guild_id):
        """Fetch detailed guild information including channels, roles, and members."""
        return await self.gate.exec_req(api.Guild.view(guild_id))

    async def ban_user(self, user_id: int, duration: int, reason: str, room_id: str):
        """Ban a user from the guild."""
        return await self.gate.exec_req(api.Guild.ban(duration, reason, room_id, user_id))

    async def unban_user(self, user_id: int, room_id: str):
        """Unban a user from the guild."""
        return await self.gate.exec_req(api.Guild.ban(0, "", room_id, user_id))


    # guild roles related
    async def fetch_roles_list(self, room_id):
        return await self.gate.exec_req(api.GuildRole.list(room_id))

    async def create_role(self, name, room_id, permissions, type=GuildRoleTypes.DEFAULT, hoist=False,
                          icon=None, color=None, color_list=None, position=None):
        data = {
            'name': name,
            'room_id': room_id,
            'permissions': permissions,
            'type': type,
            'hoist': hoist,
            'icon': icon,
            'color': color,
            'color_list': color_list,
            'position': position
        }
        return await self.gate.exec_req(api.GuildRole.update(**{k: v for k, v in data.items() if v is not None}))

    async def update_role(self, role_id, room_id, name, permissions, type=GuildRoleTypes.DEFAULT,
                          hoist=False,icon=None, color=None, color_list=None, position=None):
        data = {
            'role_id': role_id,
            'room_id': room_id,
            'name': name,
            'permissions': permissions,
            'type': type,
            'hoist': hoist,
            'icon': icon,
            'color': color,
            'color_list': color_list,
            'position': position
        }
        return await self.gate.exec_req(api.GuildRole.update(**{k: v for k, v in data.items() if v is not None}))

    async def delete_role(self, role_id, room_id):
        return await self.gate.exec_req(api.GuildRole.delete(role_id, room_id))

    async def grant_role(self, user_id, role_id, room_id):
        return await self.gate.exec_req(api.GuildRole.grant(user_id, role_id, room_id))

    async def revoke_role(self, user_id, role_id, room_id):
        return await self.gate.exec_req(api.GuildRole.revoke(user_id, role_id, room_id))


    # guild emoji related
    async def fetch_emoji_list(self, room_id):
        return await self.gate.exec_req(api.GuildEmoji.list(room_id))

    async def delete_emoji(self, emoji_id, room_id):
        return await self.gate.exec_req(api.GuildEmoji.delete(emoji_id, room_id))

    async def edit_emoji(self, emoji_id, name, room_id):
        return await self.gate.exec_req(api.GuildEmoji.edit(emoji_id, name, room_id))


    # asset related
    async def upload(self, file):
        """
        :param file: file path or binary data
        """
        if isinstance(file, str):
            with open(file, 'rb') as f:
                res = await self.gate.exec_req(api.File.upload(f))
        else:
            res = await self.gate.exec_req(api.File.upload(file))
        return res['url']

    async def requestor(self, method, endpoint, **kwargs):
        return await self.gate.request(method, endpoint, **kwargs)

    async def start(self):
        self.session = aiohttp.ClientSession()
        await asyncio.gather(self.gate.run())



