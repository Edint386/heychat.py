# guild.py

class Guild:
    def __init__(self, data):
        self.id = data.get('room_id')
        self.name = data.get('room_name', None)
