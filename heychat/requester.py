import aiohttp
import random

from .api import _Req


class Requester:
    """
    Handles the lowest-level HTTP request logic.
    """

    def __init__(self, token):
        self.token = token
        self.base_url = 'https://chat.xiaoheihe.cn'
        self.session = None
        self.default_headers = {
            'token': token
        }
        self.default_params = {
            'client_type': 'heybox_chat',
            'x_client_type': 'web',
            'os_type': 'web',
            'x_os_type': 'bot',
            'x_app': 'heybox_chat',
            'chat_os_type': 'bot',
            'chat_version': '1.24.5'
        }

    class APIRequestFailed(Exception):
        def __init__(self, method, url, status, message):
            self.method = method
            self.url = url
            self.status = status
            self.message = message
            super().__init__(f"Request {self.method} {self.url} failed with status {self.status}: {self.message}")

    async def request(self, method, route, headers=None, params=None, **kwargs):
        """
        Executes a raw HTTP request.
        """
        url = route
        headers = headers or {}
        params = params or {}
        # Merge default headers and params
        merged_headers = {**self.default_headers, **headers}
        merged_params = {**self.default_params, **params}
        merged_params['heychat_ack_id'] = random.randint(100000, 999999)

        if not self.session:
            await self.initialize_session()

        async with self.session.request(method, url, headers=merged_headers, params=merged_params, **kwargs) as resp:
            response_data = await resp.json()
            if resp.status != 200 or response_data.get("status") == "failed":
                status = response_data.get('err_code', resp.status)
                message = response_data.get('msg', 'Unknown Error')
                raise self.APIRequestFailed(method, url, status, message)
            return response_data

    async def initialize_session(self):
        self.session = aiohttp.ClientSession()

    async def exec_req(self, r: _Req):
        """_Req -> raw request"""
        return await self.request(r.method, r.route, **r.params)
