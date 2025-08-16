from typing import Union

from .channel import public_channel_factory, PublicChannel, PublicTextChannel, PublicVoiceChannel, PrivateChannel
from .guild import Guild


def is_private_message(data):
    """判断是否为私聊消息"""
    # 检查是否缺少频道信息
    has_channel_info = ('channel_base_info' in data or 
                       ('channel_id' in data and 'channel_name' in data and 'channel_type' in data))
    
    # 检查是否有to_user_id字段（机器人发出的私聊消息）
    has_to_user_id = 'to_user_id' in data
    
    # 检查消息类型是否为USER_IM_MESSAGE（私聊消息事件）
    is_user_im_type = data.get('type') == 'USER_IM_MESSAGE'
    
    # 如果没有频道信息，或者有to_user_id字段，或者是USER_IM_MESSAGE类型，则认为是私聊消息
    return not has_channel_info or has_to_user_id or is_user_im_type


class Context:
    def __init__(self, data, gate):
        if is_private_message(data):
            sender_info = data.get('sender_info') or data
            self.channel: PrivateChannel = PrivateChannel(sender_info, gate)
            self.guild = None  
        else:
            self.guild: Guild = Guild(data.get('room_base_info'), gate)
            self.channel: Union[PublicTextChannel, PublicVoiceChannel] = public_channel_factory(data, gate)
