import functools
import aiohttp


class _Req:
    def __init__(self, method, route, params):
        self.method = method
        self.route = route
        self.params = params


def req(method: str, route: str, **http_fields):
    """Decorator to create API request methods."""

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
            # 处理请求参数
            payload = _merge_params(method, http_fields, params)
            return _Req(method, base_url + route, payload)


        return wrapper

    return decorator


def _merge_params(method: str, http_fields: dict, req_args: dict) -> dict:
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
    base_url: str = 'https://chat.xiaoheihe.cn'

    # 发送消息
    @classmethod
    @req('POST', '/chatroom/v2/channel_msg/send')
    def create(self, channel_id, msg_type, room_id, msg=None, **kwargs):
        """Send a message to a channel."""
        pass

    @classmethod
    @req('POST', '/chatroom/v2/channel_msg/update')
    def update(self, msg_id, msg, room_id, channel_id, **kwargs):
        """Update existed message"""
        pass


class File:
    base_url: str = 'https://chat-upload.xiaoheihe.cn'

    # 上传文件
    @classmethod
    @req('POST', '/upload', headers={'Content-Type': 'multipart/form-data'})
    def upload(self,file):
        """Upload a file."""
        pass

    # 可以在这里添加更多的 API 方法

