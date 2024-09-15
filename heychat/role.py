# role.py

class Role:
    def __init__(self, **kwargs):
        self.role_id: str = kwargs.get("role_id", str())
        self.name: str = kwargs.get("name", "")
        # self.color: int = kwargs.get("color", 0)
        # self.position: int = kwargs.get("position", 0)
        # self.hoist: int = kwargs.get("hoist", 0)
        # self.mentionable: int = kwargs.get("mentionable", 0)
        # self.permissions: int = kwargs.get("permissions", 0)