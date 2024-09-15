# _types.py
from enum import IntEnum


class MessageTypes(IntEnum):
    IMG = 3
    MD = 4
    MD_WITH_MENTION = 10


class EventTypes:
    pass
    # JOINED_GUILD = 'JOINED_GUILD'
    # 其他事件类型


class ChannelTypes(IntEnum):
    VOICE = 0
    TEXT = 1
    ANNOUNCEMENT = 2
    CATEGORY = 3
    TEMPORARY = 4
    TEMPOR_GENERATOR = 5
