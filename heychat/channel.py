from typing import Union

from ._types import ChannelTypes, MessageTypes
from . import api
from .gateway import Gateway
from .mdmessage import MDMessage, Element


class PublicChannel:
    def __init__(self, data, gate):
        channel_info = data.get('channel_base_info')

        self.id: str = channel_info.get('channel_id')
        self.name: str = channel_info.get('channel_name')
        self.type: ChannelTypes = ChannelTypes(channel_info.get('channel_type')) if 'channel_type' in data else None

        self.guild_id: str = data.get("room_base_info").get('room_id')  # 用于 bot.client.send
        self.gate: Gateway = gate  # 添加 gateway 实例


class PublicTextChannel(PublicChannel):
    def __init__(self, data, gate):
        super().__init__(data, gate)

    async def send(self, content: Union[str, MDMessage], msg_type=MessageTypes.MD_WITH_MENTION, **kwargs):
        if isinstance(content, MDMessage):
            if content.count() == 1 and isinstance(content[0], Element.Image):
                img_url = content[0].src
                req = api.Message.create(self.id, MessageTypes.IMG, self.guild_id, img=img_url, **content.extra_info)
            else:
                req = api.Message.create(self.id, MessageTypes.MD_WITH_MENTION, self.guild_id, msg=str(content),
                                         **content.extra_info)
        else:
            req = api.Message.create(self.id, msg_type, self.guild_id, msg=content, **kwargs)
        return await self.gate.exec_req(req)


class PublicVoiceChannel(PublicChannel):
    def __init__(self, data, gate):
        super().__init__(data, gate)


class PrivateChannel(PublicTextChannel):
    def __init__(self, data, gate):
        super().__init__(data, gate)

    async def send(self, content, msg_type=MessageTypes.MD_WITH_MENTION):
        # 当前暂无该接口
        raise NotImplementedError


def public_channel_factory(data, gate) -> Union[PublicTextChannel, PublicVoiceChannel]:
    channel_info = data.get('channel_base_info')
    channel_type = ChannelTypes(channel_info.get('channel_type'))
    if channel_type == ChannelTypes.TEXT:
        return PublicTextChannel(data, gate)
    elif channel_type == ChannelTypes.VOICE:
        return PublicVoiceChannel(data, gate)
    else:
        raise NotImplementedError(f"Channel type {channel_type} is not implemented yet.")
