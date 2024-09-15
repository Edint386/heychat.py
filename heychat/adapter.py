import json


def adapt_type_5_message(type_5_message):
    # adap
    # Extract relevant fields from the Type 5 message
    data = type_5_message["data"]["addition"]
    data = json.loads(data) if data else None
    data = data["bot_command"] if data else None
    type_50_message = {
        "sequence": type_5_message["sequence"] - 10,  # Example: Adjust the sequence slightly
        "type": "50",
        "online_state": type_5_message["data"]["online_state"],
        "notify_type": "",
        "data": {
            "msg": type_5_message["data"]["msg"],
            "bot_id": data["bot_id"] if data else None,
            "channel_base_info": {
                "channel_id": type_5_message["data"]["channel_id"],
                "channel_name": type_5_message["data"]["channel_name"],
                "channel_type": type_5_message["data"]["channel_type"]
            },
            "command_info": {
                "id": data["command_info"]["id"],
                "name": data["command_info"]["name"],
                "options": data["command_info"]["options"],
                "type": data["command_info"]["type"]
            } if data else None,
            "msg_id": type_5_message["data"]["msg_id"],
            "room_base_info": {
                "room_avatar": "",  # Type 50 has empty room_avatar in the example
                "room_id": type_5_message["data"]["room_id"],
                "room_name": None  # Example: Static room name (can be made dynamic)
            },
            "send_time": type_5_message["data"]["send_time"],
            "sender_info": {
                "avatar": type_5_message["data"]["avatar"],
                "avatar_decoration": type_5_message["data"]["avatar_decoration"],
                "bot": type_5_message["data"]["bot"],
                "level": type_5_message["data"]["level"],
                "medals": type_5_message["data"]["medals"],
                "nickname": type_5_message["data"]["nickname"],
                "roles": type_5_message["data"]["roles"],
                "room_nickname": type_5_message["data"]["room_nickname"],
                "tag": type_5_message["data"]["tag"],
                "user_id": type_5_message["data"]["user_id"]
            }
        },
        "timestamp": type_5_message["timestamp"]
    }

    return type_50_message
