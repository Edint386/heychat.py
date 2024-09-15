from .channel import public_channel_factory, PublicChannel
from .guild import Guild

class Context:
    def __init__(self, data, gate):
        self.guild: Guild = Guild(data)
        self.channel: PublicChannel = public_channel_factory(data, gate)