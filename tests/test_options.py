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

        return _res

    async def test_create_option(self):
        async with httpx.AsyncClient(app=self.app, base_url='https://test') as client:
            _res: Response = await client.post(
                '/options',
                json={
                    'key': 'test',
                    'value': {'test': 1}
                }
            )
