# event.py
import json

from ._types import EventTypes
from .channel import public_channel_factory
from .guild import Guild
from .user import User

EVENT_TYPE_MAP = {}

def register_event(event_type):
    def decorator(cls):
        EVENT_TYPE_MAP[event_type] = cls
        return cls
    return decorator

class Event:
    def __init__(self, data, gate):
        self.type = data.get('type')
        self.notify_type = data.get('notify_type', '')
        self.data = data.get('data')
        self.timestamp = data.get('timestamp')
        self.gate = gate
        self.event_type = None

    def determine_event_type(self):
        return None

@register_event('5003')
class ReactionEvent(Event):
    def __init__(self, data, gate):
        super().__init__(data, gate)
        self.channel_id = self.data.get('channel_id')
        self.guild_id = self.data.get('room_id')
        self.msg_id = self.data.get('msg_id')
        self.user_id = self.data.get('user_id')
        self.emoji = self.data.get('emoji')
        self.is_add = self.data.get('is_add') == 1
        self.event_type = self.determine_event_type()

    def determine_event_type(self):
        if self.is_add:
            return EventTypes.ADDED_REACTION
        else:
            return EventTypes.DELETED_REACTION

@register_event('3001')
class GuildMemberEvent(Event):
    def __init__(self, data, gate):
        super().__init__(data, gate)
        self.user_info = self.data.get('user_info', {})
        self.state = self.data.get('state')
        self.event_type = self.determine_event_type()

        self.user = User(self.user_info)
        self.guild = Guild(self.data.get('room_base_info', {}), gate)

    def determine_event_type(self):
        if self.state == 1:
            return EventTypes.JOINED_GUILD
        elif self.state == 0:
            return EventTypes.LEFT_GUILD
        else:
            return None

@register_event('card_message_btn_click')
class BtnClickEvent(Event):
    def __init__(self, data, gate):
        super().__init__(data, gate)
        self.event_type = EventTypes.BTN_CLICKED

        self.channel = public_channel_factory(self.data, gate)
        self.guild = Guild(self.data.get('room_base_info', {}), gate)
        self.user = User(self.data.get('sender_info', {}))

        self.text = self.data.get('text')
        self.value = self.data.get('value')
        self.btn_event_type = self.data.get('event')

        self.msg_id = self.data.get('msg_id')
        self.msg_timestamp = self.data.get('send_time')





def create_event(data, gate):
    event_type = data.get('type')
    event_class = EVENT_TYPE_MAP.get(event_type, Event)
    return event_class(data, gate)
