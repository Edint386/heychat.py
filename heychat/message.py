# message.py

import json
import re
from typing import Union

from .mdmessage import MDMessage
from ._types import MessageTypes
from .user import User
from .context import Context


class Message:
    def __init__(self, data, bot):

        self.id = data.get('msg_id')
        self.content = data.get('msg', None)
        self.author = User(data.get("sender_info"))
        # 传递 gateway 实例
        self.ctx = Context(data, bot.client.gate)
        self.bot = bot
        self.msg_timestamp = data.get('send_time')
        self.row_command_info = data.get('command_info', None)
        self.command = None
        self.command_option_values = []  # 存储命令选项的值，保持顺序

        # 调用解析命令的方法
        self.parse_command()

    def parse_command(self):
        # 优先尝试从 addition 字段解析
        if self.row_command_info:
            try:
                bot_command = self.row_command_info.get('name', None)
                if bot_command:
                    command_info = self.row_command_info.get('command_info', {})
                    self.command = self.row_command_info.get('name', '').lstrip('/')
                    # 调试信息
                    # print(f"Parsed command from addition: {self.command}")
                    options = self.row_command_info.get('options', [])

                    if options:
                        for option in options:
                            option_value = option.get('value')
                            self.command_option_values.append(option_value)
                        if not self.content:
                            self.content = f'''/{self.command} {" ".join([f"{i['name']}:{i['value']}" for i in options])}'''

                    # 调试信息
                    # print(f"Command option values: {self.command_option_values}")
                    return  # 成功解析命令，退出函数
            except json.JSONDecodeError as e:
                print(f"JSON decode error in parse_addition: {e}")  # 如果解析失败，打印错误

        # 如果 addition 字段没有命令信息，尝试从消息内容解析
        self.parse_command_from_content()

    def parse_command_from_content(self):
        # 使用正则表达式匹配以 '/' 开头的命令
        command_pattern = r'^/(\S+)'
        match = re.match(command_pattern, self.content)

        if match:
            self.command = match.group(1)
            # 调试信息
            # print(f"Parsed command from content: {self.command}")
            option_values = self.content.lstrip(f"/{self.command}").strip()

            for option in option_values.split():
                if ":" in option:
                    option = option.split(":")[1]
                    self.command_option_values.append(option)
                else:
                    self.command_option_values.append(option)
        else:
            pass
            # 调试信息
            # print("No command found in content.")

        # 匹配： /command option1:value1 option2:value2 ...
        # 提取但单独的value

    async def reply(self, content: Union[str,MDMessage], msg_type=MessageTypes.MD_WITH_MENTION):
        return await self.ctx.channel.send(content, msg_type)
