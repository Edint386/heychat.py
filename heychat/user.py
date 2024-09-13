# user.py

class User:
    def __init__(self, data):
        self.id = data.get('user_id')
        self.username = data.get('nickname')
        self.avatar = data.get('avatar')
        self.bot = data.get('bot', False)
        self.nickname = data.get('nickname')
        self.roles = data.get('roles', [])
        self.online = data.get('online_state', 0)
