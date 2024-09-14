# api.py
import functools
import inspect
import logging
import re
from collections import namedtuple
from typing import Callable, Tuple
import aiohttp

# 抄的khl.py 但是还没完工


API_BASE_URL = 'https://chat.xiaoheihe.cn'

_RE_ROUTE = re.compile(r'(?<!^)(?=[A-Z])')

_Req = namedtuple('_Req', ['method', 'route', 'params'])


def req(method: str, **http_fields):
    """meta-decorator

    :returns a decorator to fill func with boilerplate"""

    def _method(func: Callable):
        @functools.wraps(func)
        def req_maker(*args, **kwargs) -> _Req:
            route = _RE_ROUTE.sub('-', func.__qualname__).lower().replace('.', '/')

            # dump args into kwargs
            param_names = list(inspect.signature(func).parameters.keys())
            for i, arg in enumerate(args):
                kwargs[param_names[i].lstrip('_')] = arg

            params = _merge_params(method, http_fields, kwargs)
            return _Req(method, route, params)

        return req_maker

    return _method


def _merge_params(method: str, http_fields: dict, req_args: dict) -> dict:
    payload = req_args
    payload_key = 'params'  # default payload_key: params=
    if method == 'POST':
        payload_key = 'json'  # POST: in default json=

        content_type = http_fields.get('headers', {}).get('Content-Type', None)
        if content_type == 'multipart/form-data':
            payload_key, payload = _build_form_payload(req_args)
            # headers of form-data req are delegated to aiohttp
            http_fields = _remove_content_type(http_fields)
        elif content_type is not None:
            raise ValueError(f'unrecognized Content-Type {content_type}')

    params = {payload_key: payload}
    params.update(http_fields)
    return params


def _remove_content_type(http_fields: dict) -> dict:
    """in some situation, such as content-type=multipart/form-data,
    content-type should be delegated to aiohttp to auto-generate,
    thus content-type is required to be removed in http_fields
    """
    if http_fields.get('headers', {}).get('Content-Type', None) is not None:
        http_fields = http_fields.copy()
        http_fields['headers'] = http_fields.get('headers', {}).copy()
        del http_fields['headers']['Content-Type']
    return http_fields


def _build_form_payload(req_args: dict) -> Tuple[str, aiohttp.FormData]:
    data = aiohttp.FormData()
    for name, value in req_args.items():
        data.add_field(name, value)
    return 'data', data


class Guild:
    pass


class Chatroom
    pass


class Message:
    pass


class APIEndpoints:
    SEND_MESSAGE = '/chatroom/v2/channel_msg/send'
    UPLOAD_MEDIA = '/upload'
