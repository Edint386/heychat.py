# user.py

class User:
    def __init__(self, data):
        basic_info = data.get('user_base_info', {})
        self.id = basic_info.get('user_id')
        self.username = basic_info.get('nickname',None)
        self.avatar = basic_info.get('avatar', None)
        self.bot = basic_info.get('bot', False)
        self.nickname = basic_info.get('room_nickname',None)
        if not self.nickname:
            self.nickname = self.username
        self.roles = basic_info.get('roles', [])
        self.tags = basic_info.get('tag', None)
        self.level = basic_info.get('level', 0)
        self.online = basic_info.get('online_state', 0)
