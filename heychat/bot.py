import asyncio
from .gateway import Gateway
from .client import Client
from .receiver import Receiver


class Bot:
    def __init__(self, token):
        self.token = token
        self.client = Client(token,Gateway(token,Receiver(token,self)))
        self.commands = {}
        self.event_handlers = {}
        self.loop = asyncio.get_event_loop()

    def command(self, name, alias=None):
        if alias is None:
            alias = []
        def decorator(func):
            all_names = [name] + alias
            for cmd_name in all_names:
                self.commands[cmd_name] = func
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
        await self.client.start()
        await asyncio.Event().wait()

    def run(self):
        self.loop.run_until_complete(self.start())