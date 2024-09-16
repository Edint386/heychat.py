from typing import Union

from .channel import public_channel_factory, PublicChannel, PublicTextChannel, PublicVoiceChannel
from .guild import Guild


class Context:
    def __init__(self, data, gate):
        self.guild: Guild = Guild(data.get('room_base_info'))
        self.channel: Union[PublicTextChannel, PublicVoiceChannel] = public_channel_factory(data, gate)
