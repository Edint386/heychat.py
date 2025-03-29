import json


def adapt_type_5_message(type_5_message):
    # adap
    # Extract relevant fields from the Type 5 message
    try:
        msg_data = type_5_message.get("data", {})
        addition = msg_data.get("addition", "")
        parsed_addition = json.loads(addition) if addition else None
        command_info = parsed_addition.get("bot_command_info") if parsed_addition else None
        if command_info and not command_info.get("options"):
            command_info = None

        type_50_message = {
            "sequence": type_5_message.get("sequence", 0) - 10,  # Example: Adjust the sequence slightly
            "type": "50",
            "online_state": msg_data.get("online_state", ""),
            "notify_type": "",
            "data": {
                "msg": msg_data.get("msg", ""),
                "bot_id": command_info.get("bot_id") if command_info else None,
                "channel_base_info": {
                    "channel_id": msg_data.get("channel_id", ""),
                    "channel_name": msg_data.get("channel_name", ""),
                    "channel_type": msg_data.get("channel_type", "")
                },
                "command_info": {
                    "id": command_info.get("command_info", {}).get("id", ""),
                    "name": command_info.get("command_info", {}).get("name", ""),
                    "options": command_info.get("command_info", {}).get("options", []),
                    "type": command_info.get("command_info", {}).get("type", "")
                } if command_info and command_info.get("command_info") else None,
                "msg_id": msg_data.get("msg_id", ""),
                "room_base_info": {
                    "room_avatar": "",  # Type 50 has empty room_avatar in the example
                    "room_id": msg_data.get("room_id", ""),
                    "room_name": None  # Example: Static room name (can be made dynamic)
                },
                "send_time": msg_data.get("send_time", 0),
                "sender_info": {
                    "avatar": msg_data.get("avatar", ""),
                    "avatar_decoration": msg_data.get("avatar_decoration", ""),
                    "bot": msg_data.get("bot", False),
                    "level": msg_data.get("level", 0),
                    "medals": msg_data.get("medals", []),
                    "nickname": msg_data.get("nickname", ""),
                    "roles": msg_data.get("roles", []),
                    "room_nickname": msg_data.get("room_nickname", ""),
                    "tag": msg_data.get("tag", ""),
                    "user_id": msg_data.get("user_id", "")
                }
            },
            "timestamp": type_5_message.get("timestamp", 0)
        }

        return type_50_message
    except Exception as e:
        # 出现任何错误时，记录错误并返回一个基本结构
        print(f"Error adapting type 5 message: {e}")
        # 返回一个最小化的消息结构，确保必要的字段存在
        return {
            "sequence": type_5_message.get("sequence", 0) - 10 if isinstance(type_5_message, dict) else 0,
            "type": "50",
            "online_state": "",
            "notify_type": "",
            "data": {
                "msg": "",
                "bot_id": None,
                "channel_base_info": {"channel_id": "", "channel_name": "", "channel_type": ""},
                "command_info": None,
                "msg_id": "",
                "room_base_info": {"room_avatar": "", "room_id": "", "room_name": None},
                "send_time": 0,
                "sender_info": {
                    "avatar": "", "avatar_decoration": "", "bot": False, "level": 0,
                    "medals": [], "nickname": "", "roles": [], "room_nickname": "",
                    "tag": "", "user_id": ""
                }
            },
            "timestamp": 0
        }
