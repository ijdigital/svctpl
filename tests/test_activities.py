import httpx
from httpx import Response
from typing import Dict, List, AnyStr, Optional

from .test_base import TestBase


class TestOption(TestBase):

    async def get_option(self, params: Optional[Dict] = None) -> Response:
        if not params:
            params: Dict = dict()

        async with httpx.AsyncClient(app=self.app, base_url='https://test') as client:
            _res: Response = await client.get(
                '/option',
                params=params
            )

        try:
            return _res
        except Exception:
            raise

    async def test_create_option(self):
        async with httpx.AsyncClient(app=self.app, base_url='https://test') as client:
            _res: Response = await client.post(
                '/options',
                json={
                    'key': 'test',
                    'value': {'test': 1}
                }
            )

            # assert 'amount' in _res.json()
            # assert _res.json()['amount'] == -5000
            # ...
    # 
    # async def test_get_option(self):
    #     _response = await self.api('/option', 'GET')
    #     ...
    # 
    #     _response: Response = await self.get_option()
    # 
    # async def test(self):
    #     async with httpx.AsyncClient(app=self.app, base_url='https://test') as client:
    #         _res: Response = await client.get('/service')
