# guild.py
from heychat import api
from ._types import GuildRoleTypes


class Guild:
    def __init__(self, data, gate):
        self.id = data.get('room_id')
        self.name = data.get('room_name', None)
        self.gate = gate

    async def fetch_roles_list(self):
        await self.gate.exec_req(api.GuildRole.list(self.id))

    async def create_role(self, role_id, name, permissions, type=GuildRoleTypes.DEFAULT, hoist=False, icon=None,
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
