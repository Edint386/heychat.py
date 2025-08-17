# channel.py
import json
from typing import Union, Optional
import uuid

from ._types import ChannelTypes, MessageTypes
from . import api
from .gateway import Gateway
from .mdmessage import MDMessage


class PublicChannel:
    def __init__(self, data, gate):
        channel_info = data.get('channel_base_info')

        self.id: str = channel_info.get('channel_id')
        self.name: str = channel_info.get('channel_name')
        self.type: ChannelTypes = ChannelTypes(channel_info.get('channel_type')) if 'channel_type' in data else None

        self.guild_id: str = data.get("room_base_info").get('room_id')  # 用于 bot.client.send
        self.gate: Gateway = gate  # 添加 gateway 实例

    async def send(self, content: Union[str, MDMessage], msg_type = MessageTypes.MD_WITH_MENTION, **kwargs):
        if isinstance(content, dict):
            req = api.Message.create(self.id, MessageTypes.CARD, self.guild_id, msg=json.dumps(content), **kwargs)
        elif isinstance(content, MDMessage):
            req = api.Message.create(self.id, MessageTypes.MD_WITH_MENTION, self.guild_id, msg=str(content),
                                         **content.extra_info)
        else:
            # 普通文本消息
            req = api.Message.create(self.id, msg_type, self.guild_id, msg=content, **kwargs)
        return await self.gate.exec_req(req)

    async def update_message(self, msg_id:str, content:Union[str, MDMessage],
                             msg_type = MessageTypes.MD_WITH_MENTION, reply_id=None, **kwargs):
        data = {
            'msg_id': msg_id,
            'room_id': self.guild_id,
            'channel_id': self.id,
            'msg_type': msg_type,
            **kwargs}

        if isinstance(content, MDMessage):
            data = {**data, **content.extra_info}
            content = str(content)
        elif isinstance(content, dict):
            data['msg_type'] = MessageTypes.CARD
            content = json.dumps(content)

        data['msg'] = str(content)

        if reply_id:
            data['reply_id'] = reply_id

        return await self.gate.exec_req(api.Message.update(**data))

    async def delete_message(self, msg_id:str):
        return await self.gate.exec_req(api.Message.delete(msg_id, self.guild_id, self.id))

    async def add_reaction(self, msg_id:str, emoji:str):
        return await self.gate.exec_req(api.Message.reply_emoji(msg_id, emoji,1, self.id, self.guild_id))

    async def delete_reaction(self, msg_id:str, emoji:str):
        return await self.gate.exec_req(api.Message.reply_emoji(msg_id, emoji,0, self.id, self.guild_id))


class PublicTextChannel(PublicChannel):
    def __init__(self, data, gate):
        super().__init__(data, gate)




class PublicVoiceChannel(PublicChannel):
    def __init__(self, data, gate):
        super().__init__(data, gate)

    async def kick_out(self, user_id: int):
        """Kick out a user from this voice channel."""
        return await self.gate.exec_req(api.Channel.kick_out(
            to_user_id=user_id,
            heybox_id=user_id,
            room_id=self.guild_id, 
            channel_id=self.id
        ))

    async def move_user(self, user_ids: Union[int, list], target_channel_id: str):
        """Move users from this voice channel to another channel."""
        if isinstance(user_ids, int):
            user_ids = [user_ids]
        return await self.gate.exec_req(api.Channel.move_user(
            origin_channel_id=self.id,
            to_user_ids=user_ids,
            room_id=self.guild_id,
            channel_id=target_channel_id
        ))

    async def start_stream(self, stream_url: str, operator: int = 18661718, volume: int = 100, 
                          seek_second: Optional[int] = None, repeat_num: int = 1, 
                          max_duration: Optional[int] = None):
        """开始向此语音频道推流。
        
        Args:
            max_duration: 最大播放时长（分钟），范围[。设置后会自动将repeat_num设为-1进行循环播放。
        """
        # 当有max_duration时自动把repeat_num设为-1
        if max_duration is not None:
            repeat_num = -1
            
        result = await self.gate.exec_req(api.ChannelStream.start_stream(
            room_id=self.guild_id,
            channel_id=self.id,
            stream_url=stream_url,
            operator=operator,
            volume=volume,
            callback_url=None,
            seek_second=seek_second,
            repeat_num=repeat_num,
            max_duration=max_duration
        ))
        
        return result['task_id']


class PrivateChannel:
    """私聊频道类，代表与某个用户的私聊会话"""
    
    def __init__(self, user_data, gate):
        from .user import User  # 避免循环导入
        
        # 如果传入的是User对象，直接使用；否则创建User对象
        if hasattr(user_data, 'id'):
            self.user = user_data
        else:
            self.user = User(user_data, gate)
            
        self.gate = gate
        self.id = str(self.user.id)  # 使用用户ID作为频道ID
        self.name = f"私聊-{self.user.nickname or self.user.username}"
        self.type = "private"  # 私聊频道类型标识
        
    async def send(self, content: Union[str, dict, 'MDMessage'], msg_type=MessageTypes.MD_WITH_MENTION, **kwargs):
        """发送私聊消息"""
        # 生成唯一的 heychat_ack_id
        if 'heychat_ack_id' not in kwargs:
            kwargs['heychat_ack_id'] = str(uuid.uuid4())
            
        return await self.user.send(content, msg_type=msg_type, **kwargs)
    
    async def delete_message(self, msg_id: str):
        """删除私聊消息 - 私聊可能不支持此操作"""
        raise NotImplementedError("私聊消息删除功能暂不支持")
        
    async def add_reaction(self, msg_id: str, emoji: str):
        """给私聊消息添加表情 - 私聊可能不支持此操作"""
        raise NotImplementedError("私聊消息表情功能暂不支持")
        
    async def delete_reaction(self, msg_id: str, emoji: str):
        """删除私聊消息表情 - 私聊可能不支持此操作"""
        raise NotImplementedError("私聊消息表情功能暂不支持")
        
    async def update_message(self, msg_id: str, content: Union[str, 'MDMessage'], 
                           msg_type=MessageTypes.MD_WITH_MENTION, reply_id=None, **kwargs):
        """更新私聊消息 - 私聊可能不支持此操作"""
        raise NotImplementedError("私聊消息更新功能暂不支持")


def public_channel_factory(data, gate) -> Union[PublicTextChannel, PublicVoiceChannel]:
    channel_info = data.get('channel_base_info')
    channel_type_value = channel_info.get('channel_type')
    
    # 检查channel_type是否有效，如果无效则默认为文本频道(1)
    if channel_type_value == '' or channel_type_value is None:
        channel_type = ChannelTypes.TEXT  # 默认为文本频道
    else:
        try:
            channel_type = ChannelTypes(channel_type_value)
        except ValueError:
            # 如果值无效，也默认为文本频道
            channel_type = ChannelTypes.TEXT
    
    if channel_type == ChannelTypes.TEXT:
        return PublicTextChannel(data, gate)
    elif channel_type == ChannelTypes.VOICE:
        return PublicVoiceChannel(data, gate)
    else:
        # 对于其他类型，也返回文本频道
        return PublicTextChannel(data, gate)
