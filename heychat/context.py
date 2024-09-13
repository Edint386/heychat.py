# context.py

from .guild import Guild
from .channel import Channel

class Context:
    def __init__(self, data):
        self.guild = Guild(data)
        self.channel = Channel(data)
