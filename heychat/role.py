# role.py

from ._types import GuildRoleTypes

class Role:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id", "")
        self.name: str = kwargs.get("name", "")
        self.icon: str = kwargs.get("icon", "")
        self.color: int = kwargs.get("color", 0)
        self.color_list: list = kwargs.get("color_list", [])
        self.position: int = kwargs.get("position", 0)
        self.permissions: int = kwargs.get("permissions", 0)
        self.room_id = kwargs.get("room_id", "")
        self.type: GuildRoleTypes = GuildRoleTypes(kwargs.get("type", 0))
        self.hoist: bool = bool(kwargs.get("hoist", 0))
        self.creator: bool = bool(kwargs.get("creator", 0))
        self.create_time: int = kwargs.get("create_time", 0)




    def has_permission(self, bit_value: int) -> bool:
        return self.permissions & bit_value == bit_value
