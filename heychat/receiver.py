# receiver.py
import traceback

import aiohttp
import asyncio
import json

from .message import Message
from .event import Event, create_event
import ssl
import logging
from .adapter import adapt_type_5_message
from collections import OrderedDict


class LimitedDict(OrderedDict):
    def __init__(self, max_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_size = max_size

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.max_size:
            self.popitem(last=False)


class Receiver:
    def __init__(self, token, bot):
        self.token = token
        self.bot = bot
        self.ws_url = 'wss://chat.xiaoheihe.cn/chatroom/ws/connect'
        self.session = None
        self.headers = {
            'token': token
        }
        self.params = {
            'client_type': 'heybox_chat',
            'x_client_type': 'web',
            'os_type': 'web',
            'x_os_type': 'bot',
            'x_app': 'heybox_chat',
            'chat_os_type': 'bot',
            'chat_version': '1.24.5'
        }
        self.gate = bot.client.gate
        self.is_connected = False
        self.close = False
        self.message_queue = asyncio.Queue()
        self.ping_interval = 30  # 心跳间隔
        self.logger = logging.getLogger(__name__)
        self.messages = LimitedDict(20)

    async def connect(self):
        self.logger.info("Connecting to WebSocket server...")
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        try:
            self.ws = await self.session.ws_connect(
                self.ws_url,
                headers=self.headers,
                params=self.params,
                ssl=ssl_context
            )
            self.is_connected = True
            self.logger.info("WebSocket connection established.")
            # 启动接收、处理和心跳任务，并保存任务对象
            self.receive_task = asyncio.create_task(self.receive())
            self.handle_task = asyncio.create_task(self.handle())
            self.heartbeat_task = asyncio.create_task(self.heartbeat())
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            await self.reconnect()

    async def send_ping(self):
        await self.ws.send_str('PING')

    async def heartbeat(self):
        self.logger.info("Heartbeat task started.")
        while not self.close:
            await asyncio.sleep(self.ping_interval)
            if not self.is_connected:
                continue
            try:
                await self.send_ping()
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                await self.reconnect()
                break

    async def receive(self):
        self.logger.info("Receive task started.")
        while not self.close:
            try:
                msg = await self.ws.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.message_queue.put(msg.data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self.logger.warning("WebSocket closed.")
                    await self.reconnect()
                    continue  # 改为 continue 而不是 break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.logger.error("WebSocket error.")
                    await self.reconnect()
                    continue  # 改为 continue 而不是 break
            except Exception as e:
                self.logger.error(f"Receive error: {e}")
                await self.reconnect()
                continue  # 改为 continue 而不是 break

    async def reconnect(self):
        self.is_connected = False
        await asyncio.sleep(5)  # 重连前等待
        self.logger.info("Reconnecting to WebSocket server...")
        await self.connect()

    async def handle(self):
        self.logger.info("Handle task started.")
        while not self.close:
            try:
                message = await self.message_queue.get()
                if message in ['PONG', 'pong'] or message.startswith('PONG'):
                    continue
                try:
                    data = json.loads(message)
                    # print(data)
                    asyncio.create_task(self.handle_message(data))
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to decode JSON: {e}")
                    continue  # 解析 JSON 失败，继续处理下一条消息
            except Exception as e:
                print(traceback.format_exc())
                self.logger.error(f"Handle error: {e}")
                continue  # 捕获异常后继续处理下一条消息

    async def close_connection(self):
        self.close = True
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()

    async def handle_message(self, data):
        # 检查消息 ID，防止重复处理
        if isinstance(data, str):
            return
        inner_data = data.get('data', {})
        # print(data)
        if isinstance(inner_data, str):
            return
        msg_id = inner_data.get('msg_id', data.get('sequence'))

        if msg_id in self.messages.keys():
            return

        event_type = data.get('type')

        if event_type == '50' and not data['data'].get('command_info').get('id'):
            # 此情况适用于用户发生了一条未被注册的指令，50消息不会包含任何内容
            return

        if event_type == '5':
            data = adapt_type_5_message(data)
            event_type = '50'

        self.messages[msg_id] = data

        if event_type == '50':  # 消息类型
            message = Message(data['data'], self.bot)
            # 调试信息
            # print(f"Received message: {message.content}")
            # print(f"Command: {message.command}")
            # print(f"Command option values: {message.command_option_values}")

            if 'on_message' in self.bot.event_handlers:
                await self.bot.event_handlers['on_message'](message)

            if message.command:
                command_name = message.command
                # print(f"option_values: {message.command_option_values}")
                if command_name in self.bot.commands:
                    command_func = self.bot.commands[command_name]
                    # 获取命令函数的参数列表
                    from inspect import signature
                    sig = signature(command_func)
                    params = sig.parameters
                    # 构建参数列表，跳过第一个参数 msg
                    func_args = [message]  # 第一个参数是 msg
                    # 获取函数参数的数量，减去 msg 参数
                    num_params = len(params) - 1
                    # 从命令选项值中取出对应数量的值
                    option_values = message.command_option_values[:num_params]
                    func_args.extend(option_values)
                    # 如果选项值不够，用 None 填充
                    if len(option_values) < num_params:
                        func_args.extend([None] * (num_params - len(option_values)))

                    # 调试信息
                    # print(f"Calling command function: {command_name} with args: {func_args[1:]}")
                    await command_func(*func_args)
                else:
                    pass
                    # print(f"Command '{command_name}' not found in registered commands.")
        else:
            event = create_event(data, self.gate)
            handlers = self.bot.event_handlers.get('on_event', {}).get(event.event_type, [])
            for handler in handlers:
                await handler(event)

    async def start(self):
        self.session = aiohttp.ClientSession()
        await self.connect()
