# _types.py
import enum

@enum.unique
class MessageTypes(enum.Enum):
    IMG = 3
    MD = 4
    MD_WITH_MENTION = 10

class EventTypes:
    pass
    # JOINED_GUILD = 'JOINED_GUILD'
    # 其他事件类型

@enum.unique
class ChannelTypes(enum.Enum):
    VOICE = 0
    TEXT = 1
    ANNOUNCEMENT = 2
    CATEGORY = 3
    TEMPORARY = 4
    TEMPOR_GENERATOR = 5
