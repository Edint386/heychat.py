# user.py
from typing import List
from .role import Role


class User:
    def __init__(self, data):
        self.id: int = int(data.get('user_id'))
        self.username: str = data.get('nickname', None)
        self.nickname: str = data.get('room_nickname', None) or self.username
        self.avatar: str = data.get('avatar', None)
        self.bot: bool = data.get('bot', False)
        self.roles: List[Role] = [Role(id=role) for role in data.get('roles') or []]
        self.tags: list = data.get('tag', None)
        self.level: int = data.get('level', 0)
        self.online: int = data.get('online_state', 0)
