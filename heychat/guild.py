# guild.py
from heychat import api
from ._types import GuildRoleTypes


class Guild:
    def __init__(self, data, gate):
        self.id = data.get('room_id')
        self.name = data.get('room_name', None)
        self.avatar = data.get('room_avatar', None)
        self.gate = gate

    async def fetch_roles_list(self):
        await self.gate.exec_req(api.GuildRole.list(self.id))

    async def create_role(self, name, permissions, type=GuildRoleTypes.DEFAULT, hoist=False, icon=None,
                          color=None, color_list=None, position=None):
        data = {
            'room_id': self.id,
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

    async def update_role(self, role_id, name, permissions, type=GuildRoleTypes.DEFAULT, hoist=False, icon=None,
                          color=None, color_list=None, position=None):
        data = {
            'role_id': role_id,
            'room_id': self.id,
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

    async def delete_role(self, role_id):
        return await self.gate.exec_req(api.GuildRole.delete(role_id, self.id))

    async def grant_role(self, user_id, role_id):
        return await self.gate.exec_req(api.GuildRole.grant(user_id, role_id, self.id))

    async def revoke_role(self, user_id, role_id):
        return await self.gate.exec_req(api.GuildRole.revoke(user_id, role_id, self.id))

    async def fetch_emoji_list(self):
        return await self.gate.exec_req(api.GuildEmoji.list(self.id))

    async def delete_emoji(self, emoji_id):
        return await self.gate.exec_req(api.GuildEmoji.delete(emoji_id, self.id))

    async def edit_emoji(self, emoji_id, name):
        return await self.gate.exec_req(api.GuildEmoji.edit(emoji_id, name, self.id))

    async def ban_user(self, user_id: int, duration: int, reason: str):
        """Ban a user from this guild."""
        return await self.gate.exec_req(api.Guild.ban(duration, reason, self.id, user_id))

    async def unban_user(self, user_id: int):
        """Unban a user from this guild."""
        return await self.gate.exec_req(api.Guild.ban(0, "", self.id, user_id))
