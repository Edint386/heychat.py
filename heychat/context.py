from .guild import Guild
from .channel import Channel

class Context:
    def __init__(self, data, gate):
        self.guild = Guild(data)
        self.channel = Channel(data, gate)