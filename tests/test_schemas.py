import os

import pytest
import random
from typing import Optional, List, AnyStr

from schemas import *


class TestConfSchema:

    def set_database_environment(self, missing: Optional[bool] = False) -> None:
        for k in os.environ.keys():
            os.environ[k] = ''

        keys: List = ['DB_NAME', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD']

        random_element_idx = None
        if missing:
            random_element_idx: int = random.randint(0, 4)

        if random_element_idx:
            keys.pop(random_element_idx)

        for _k in keys:
            if _k != 'DB_PORT':
                os.environ[_k] = 'test'
                continue
            os.environ[_k] = '123'

    def test_DatabaseConfig_schema(self):
        self.set_database_environment()

        config_db: DatabaseConfig = DatabaseConfig()
        config_db = config_db.__dict__

        assert 'db_name' in config_db
        assert isinstance(config_db['db_name'], str)

        assert 'db_host' in config_db
        assert isinstance(config_db['db_host'], str)

        assert 'db_port' in config_db
        assert isinstance(config_db['db_port'], int)

        assert 'db_user' in config_db
        assert isinstance(config_db['db_user'], str)

        assert 'db_password' in config_db
        assert isinstance(config_db['db_password'], str)