# _types.py
from enum import IntEnum


class MessageTypes(IntEnum):
    IMG = 3
    MD = 4
    MD_WITH_MENTION = 10
    CARD = 20


# _types.py

class EventTypes:
    JOINED_GUILD = 'joined_room'
    LEFT_GUILD = 'left_room'
    ADDED_REACTION = 'added_reaction'
    DELETED_REACTION = 'deleted_reaction'
    BTN_CLICKED = 'card_message_button_click'



class GuildRoleTypes(IntEnum):
    DEFAULT = 0        # 默认角色类型
    GAME = 1           # 游戏角色类型
    BOT = 2            # 机器人角色类型
    MEMBER_ADMIN = 3   # 成员管理员类型
    TEXT_CHANNEL_ADMIN = 4  # 文本频道管理员类型
    VOICE_CHANNEL_ADMIN = 5 # 语音频道管理员类型
    COMMUNITY_BUILDER = 6   # 社区建设者类型
    SENIOR_ADMIN = 7        # 高级管理员类型
    GUEST = 254         # 访客类型
    ALL = 255     # 所有用户角色类型


class ChannelTypes(IntEnum):
    VOICE = 0
    TEXT = 1
    ANNOUNCEMENT = 2
    CATEGORY = 3
    TEMPORARY = 4
    TEMPOR_GENERATOR = 5
