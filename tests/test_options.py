import httpx
from httpx import Response
from typing import Dict, List, AnyStr, Optional

from .test_base import TestBase
from .assets import *


class TestOption(TestBase):

    async def test_get_options(self):
        _response: Response = await self.api('GET', '/options')

        assert _response.status_code == 200
        assert 'options' in _response.json()

    async def test_create_option(self):
        _response: Response = await self.api('POST', '/options', _body=body_create_option)

        assert _response.status_code == 201
        assert _response.json() == body_create_option
