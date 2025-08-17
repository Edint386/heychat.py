# user.py
from typing import List, Union
from .role import Role
from ._types import MessageTypes
from . import api
import json
from .mdmessage import MDMessage


class User:
    def __init__(self, data, gate):
        self.id: int = int(data.get('user_id'))
        self.username: str = data.get('nickname', None)
        self.nickname: str = data.get('room_nickname', None) or self.username
        self.avatar: str = data.get('avatar', None)
        self.bot: bool = data.get('bot', False)
        self.roles: List[Role] = [Role(id=role) for role in data.get('roles') or []]
        self.tags: list = data.get('tag', None)
        self.level: int = data.get('level', 0)
        self.online: int = data.get('online_state', 0)
        self.gate = gate

    async def send(self, content: Union[str, MDMessage, dict], msg_type=MessageTypes.MD_WITH_MENTION, **kwargs):
        """Send a direct message to this user."""
        if not self.gate:
            raise ValueError("Gateway is required to send messages")

        if isinstance(content, dict):
            # 卡片消息
            req = api.UserMessage.send(self.id, MessageTypes.CARD, json.dumps(content), **kwargs)
        elif isinstance(content, MDMessage):
            # MD消息
            req = api.UserMessage.send(self.id, MessageTypes.MD_WITH_MENTION, str(content), 
                                      addition=json.dumps(content.extra_info) if content.extra_info else "{}", 
                                      **kwargs)
        else:
            # 普通文本消息
            req = api.UserMessage.send(self.id, msg_type, str(content), **kwargs)
            
        return await self.gate.exec_req(req)

    async def find_current_channel(self, room_id: str):
        """Find which channel this user is currently in."""
        return await self.gate.exec_req(api.Channel.which_user(self.id, room_id))
