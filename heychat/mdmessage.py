import json
from typing import Union, Dict


class MDMessage:
    messages: list
    _cache: str

    def __init__(self, *element):
        self.messages = [*element]

    def append(self, message):
        # 将传入的内容转换为字符串并添加到列表中
        self.messages.append(message)

    def count(self):
        # 返回已添加字符串的数量
        return len(self.messages)

    def __str__(self):
        # 如果缓存为 None，更新缓存，否则直接返回缓存内容
        return ''.join([str(message) for message in self.messages])

    def __getitem__(self, index):
        # 允许通过索引访问 messages 列表中的元素
        return self.messages[index]

    def __setitem__(self, index, value):
        # 允许通过索引修改 messages 列表中的元素
        self.messages[index] = str(value)

    def __len__(self):
        # 使 len(md) 返回消息的数量
        return len(self.messages)

    def __iter__(self):
        # 使类可迭代
        return iter(self.messages)

    @property
    def extra_info(self):
        additions = []
        user_mentioned = []
        channel_mentioned = []
        for message in self.messages:
            if isinstance(message, Element.Image):
                img_info = {'url': message.src}
                if message.width:
                    img_info['width'] = message.width
                if message.height:
                    img_info['height'] = message.height
                additions.append(img_info)
            elif isinstance(message, Element.Mention):
                user_mentioned.append(message.id)
            elif isinstance(message, Element.Channel):
                channel_mentioned.append(message.id)
        info = {}
        if additions:
            info['addition'] = json.dumps({'img_files_info': additions})
        if user_mentioned:
            info['at_user_id'] = ','.join(user_mentioned)
        if channel_mentioned:
            info['at_channel_id'] = ','.join(channel_mentioned)
        return info


class Element:
    class Text:

        def __init__(self, content: str):
            self.content = content

        def __str__(self):
            return self.content

    class Image:
        src: str
        width: int
        height: int

        def __init__(self, img_url: str, width: int = None, height: int = None):
            self.src = img_url
            self.width = width
            self.height = height

        def __str__(self):
            return f'![]({self.src})'

    class Mention:
        def __init__(self, id: str):
            self.id = str(id)

        def __str__(self):
            return f'@{{id:{self.id}}}'

    class Channel:
        def __init__(self, id: str):
            self.id = id

        def __str__(self):
            return f'#{{id:{self.id}}}'
