# user.py

class User:
    def __init__(self, data):
        self.id = data.get('user_id')
        self.username = data.get('nickname',None)
        self.avatar = data.get('user_base_info', {}).get('avatar', None)
        self.bot = data.get('bot', False)
        self.nickname = data.get('nickname',None)
        if not self.nickname:
            self.nickname = self.username
        self.roles = data.get('roles', [])
        self.tags = data.get('tags', [])
        self.level = data.get('level', 0)
        self.online = data.get('online_state', 0)
