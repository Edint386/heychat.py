import functools
from uuid import uuid4
import aiohttp

class _Req:
    def __init__(self, method, route, params):
        self.method = method
        self.route = route
        self.params = params


def req(method: str, route: str, query_params=None, **http_fields):
    """Decorator to create API request methods.
    
    Args:
        method: HTTP method
        route: API route
        query_params: List of parameter names that should be sent as query parameters
        **http_fields: Additional HTTP fields like headers
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self_instance = args[0]
            base_url = getattr(self_instance, 'base_url', None)
            args = args[1:]
            if base_url is None:
                raise ValueError('base_url is not set')
            # 获取函数参数名列表
            param_names = func.__code__.co_varnames[:func.__code__.co_argcount][1:]
            # 将位置参数和关键字参数合并
            params = dict(zip(param_names, args))
            params.update(kwargs)
            if 'heychat_ack_id' in param_names and 'heychat_ack_id' not in params:
                params['heychat_ack_id'] = str(uuid4())
            # 处理请求参数
            payload = _merge_params(method, http_fields, params, query_params)

            return _Req(method, base_url + route, payload)


        return wrapper

    return decorator


def _merge_params(method: str, http_fields: dict, req_args: dict, query_params=None) -> dict:
    """Merge request parameters based on method and query_params specification.
    
    Args:
        method: HTTP method
        http_fields: Additional HTTP fields
        req_args: Request arguments from function call
        query_params: List of parameter names that should be query parameters
    """

    if query_params is None:
        payload_key = 'params'
        payload = req_args

        if method == 'POST':
            payload_key = 'json'
            content_type = http_fields.get('headers', {}).get('Content-Type', None)

            if content_type == 'multipart/form-data':
                payload_key, payload = _build_form_payload(req_args)
                http_fields = _remove_content_type(http_fields)
            elif content_type is not None and content_type != 'application/json':
                raise ValueError(f'Unrecognized Content-Type {content_type}')
        params = {payload_key: payload}
        params.update(http_fields)
        return params
    
    query_args = {}
    body_args = {}
    
    for key, value in req_args.items():
        if key in query_params:
            query_args[key] = value
        else:
            body_args[key] = value
    
    params = {}
    
    if query_args:
        params['params'] = query_args
    
    if body_args:
        if method == 'POST':
            content_type = http_fields.get('headers', {}).get('Content-Type', None)
            
            if content_type == 'multipart/form-data':
                payload_key, payload = _build_form_payload(body_args)
                params[payload_key] = payload
                http_fields = _remove_content_type(http_fields)
            elif content_type is not None and content_type != 'application/json':
                raise ValueError(f'Unrecognized Content-Type {content_type}')
            else:
                params['json'] = body_args
        else:
            if 'params' in params:
                params['params'].update(body_args)
            else:
                params['params'] = body_args
    
    params.update(http_fields)
    return params


def _remove_content_type(http_fields: dict) -> dict:
    if http_fields.get('headers', {}).get('Content-Type', None) is not None:
        http_fields = http_fields.copy()
        http_fields['headers'] = http_fields.get('headers', {}).copy()
        del http_fields['headers']['Content-Type']
    return http_fields


def _build_form_payload(req_args: dict):
    data = aiohttp.FormData()
    for name, value in req_args.items():
        data.add_field(name, value)
    return 'data', data


class Message:
    """Class containing API methods."""
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v2/channel_msg'

    # 发送消息
    @classmethod
    @req('POST', '/send')
    def create(cls, channel_id, msg_type, room_id, msg, heychat_ack_id, **kwargs):
        """Send a message to a channel."""
        pass

    @classmethod
    @req('POST', '/update')
    def update(cls, msg_id, msg, room_id, channel_id, heychat_ack_id, **kwargs):
        """Update existing message."""
        pass

    @classmethod
    @req('POST', '/delete')
    def delete(cls, msg_id, room_id, channel_id):
        """Delete a message"""
        pass

    @classmethod
    @req('POST', '/emoji/reply')
    def reply_emoji(cls, msg_id, emoji, is_add, channel_id, room_id):
        """Add/Remove emoji reaction to a message."""
        pass


class UserMessage:
    """用户私聊消息API"""
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v3/msg'

    @classmethod
    @req('POST', '/user')
    def send(cls, to_user_id, msg_type, heychat_ack_id, msg=None, img=None, addition="{}", **kwargs):
        """Send a direct message to a user."""
        pass


class GuildRole:
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v2/room_role'

    @classmethod
    @req('GET', '/roles')
    def list(cls, room_id):
        """Get roles of a room."""
        pass

    @classmethod
    @req('POST', '/create')
    def create(cls, name, room_id, permissions, type, hoist, nonce, icon, color, color_list, position):
        """Create a role."""
        pass

    @classmethod
    @req('POST', '/update')
    def update(cls, id, name, room_id, permissions, type, hoist, nonce, icon, color, color_list, position):
        """Update a role."""
        pass

    @classmethod
    @req('POST', '/delete')
    def delete(cls, role_id, room_id):
        """Delete a role."""
        pass

    @classmethod
    @req('POST', '/grant')
    def grant(cls, to_user_id, role_id, room_id):
        """Grant a role to a user."""
        pass

    @classmethod
    @req('POST', '/revoke')
    def revoke(cls, to_user_id, role_id, room_id):
        """Revoke a role from a user."""
        pass

class GuildEmoji:
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v3/msg/meme/room'

    @classmethod
    @req('GET', '/list')
    def list(cls, room_id):
        """Get emojis of a room."""
        pass

    @classmethod
    @req('POST', '/del')
    def delete(cls, path, room_id):
        """Delete an emoji."""
        pass

    @classmethod
    @req('POST', '/edit')
    def edit(cls, path, name, room_id):
        """Edit an emoji."""
        pass




class File:
    base_url: str = 'https://chat-upload.xiaoheihe.cn'

    # 上传文件
    @classmethod
    @req('POST', '/upload', headers={'Content-Type': 'multipart/form-data'})
    def upload(cls, file):
        """Upload a file."""
        pass

    # 可以在这里添加更多的 API 方法


class Channel:
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v2/channel'

    @classmethod
    @req('POST', '/kick_out', query_params=['heybox_id', 'room_id', 'channel_id'])
    def kick_out(cls, to_user_id, heybox_id=None, room_id=None, channel_id=None):
        """Kick out a user from voice channel."""
        pass


class Guild:
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v2/room'

    @classmethod
    @req('GET', '/view', query_params=['room_id'])
    def view(cls, room_id):
        """Get detailed guild information including channels, roles, and members."""
        pass


class UserMessage:
    base_url: str = 'https://chat.xiaoheihe.cn/chatroom/v3/msg'

    @classmethod
    @req('POST', '/user')
    def send(cls, to_user_id, msg_type, msg, heychat_ack_id, **kwargs):
        """Send a direct message to a user."""
        pass

