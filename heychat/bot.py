# bot.py

import asyncio
from .client import Client
from .gateway import Gateway
from ._types import EventTypes

class Bot:
    def __init__(self, token):
        self.token = token
        self.client = Client(token)
        self.gateway = Gateway(token, self)
        self.commands = {}
        self.event_handlers = {}
        self.loop = asyncio.get_event_loop()

    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator

    def on_message(self):
        def decorator(func):
            self.event_handlers['on_message'] = func
            return func
        return decorator

    def on_event(self, event_type):
        def decorator(func):
            if 'on_event' not in self.event_handlers:
                self.event_handlers['on_event'] = {}
            self.event_handlers['on_event'][event_type] = func
            return func
        return decorator

    async def start(self):
        await self.gateway.connect()
        # 等待一个永远不会完成的事件，保持程序运行
        await asyncio.Event().wait()

    def run(self):
        self.loop.run_until_complete(self.start())
