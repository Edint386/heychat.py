from .requester import Requester
from .api import _Req


class Gateway:
    def __init__(self, token, receiver):
        self.token = token
        self.requester = Requester(token)
        self.receiver = receiver

    async def request(self, method, path, **params):
        return await self.requester.request(method, path, **params)

    async def exec_req(self, r: _Req):
        """execute request, this is just a wrapper for convenience"""
        return await self.requester.exec_req(r)

    async def run(self):
        await self.receiver.start()
