# channel.py

class Channel:
    def __init__(self, data):
        self.id = data.get('channel_id')
        self.name = data.get('channel_name')
        self.type = data.get('channel_type', 1)
        self.guild_id = data.get('room_id')

    async def send(self, content):
        # 调用 Bot 的 client.send 方法
        pass
