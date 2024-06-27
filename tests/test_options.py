import httpx
from httpx import Response
from typing import Dict, List, AnyStr, Optional

from .test_base import TestBase
from .assets import *


class TestOption(TestBase):

    async def create_option(self, key: Optional[AnyStr]):
        body_create_option['key'] = key
        _response: Response = await self.api('POST', '/options', _body=body_create_option)

        return _response.json()['key']

    async def test_get_options(self):
        _response: Response = await self.api('GET', '/options')

        assert _response.status_code == 200
        assert 'options' in _response.json()

    async def test_create_option(self):
        _response: Response = await self.api('POST', '/options', _body=body_create_option)

        assert _response.status_code == 201
        assert _response.json() == body_create_option

    async def test_get_option(self):
        key: AnyStr = await self.create_option(key='get_single_option')

        _response: Response = await self.api('GET', f'/options/{key}')

        assert _response.status_code == 200
        assert _response.json()['key'] == key

    async def test_update_option(self):
        key: AnyStr = await self.create_option(key='get_single_option')

        update_value: Dict = {}
        _response: Response = await self.api('PATCH', f'/options/{key}', _body={
            'value': update_value
        })

        assert _response.status_code == 202
        assert _response.json()['value'] == update_value

