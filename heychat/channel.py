from ._types import ChannelTypes, MessageTypes
from . import api

class Channel:
    def __init__(self, data, gate):
        self.id = data.get('channel_id')
        self.name = data.get('channel_name')
        self.type = ChannelTypes(data.get('channel_type')) if 'channel_type' in data else None
        self.guild_id = data.get('room_id')  # 用于 bot.client.send
        self.gate = gate  # 添加 gateway 实例

    async def send(self, content, msg_type=MessageTypes.MD_WITH_MENTION):
        # 使用 Gateway 的 send 方法
        return await self.gate.exec_req(api.Message.create(self.id, content, msg_type.value,self.guild_id))