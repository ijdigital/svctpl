import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import asyncpg
from tortoise import Tortoise
from typing import AnyStr, Optional, Dict

from schemas import DatabaseConfig

_test: Optional[AnyStr] = os.getenv('TEST_MODE', None)
_database_to_use: Optional[AnyStr] = os.getenv('TEST_DATABASE', None)
_conn = None


@asynccontextmanager
async def lifespan(service: FastAPI) -> None:
    await startup_event()
    yield
    await shutdown_event()


def get_service() -> FastAPI:
    if hasattr(get_service, 'service'):
        return get_service.service

    service: FastAPI = FastAPI(lifespan=lifespan)
    get_service.service: FastAPI = service
    return service


async def startup_event() -> None:
    """
    Code which is executed before starting application.
    If application is in test mode it'll execute specific
    startup method for test mode.

    :return: None
    """

    if isinstance(_test, str):
        return await test_startup_event()

    DATABASE: DatabaseConfig = DatabaseConfig()

    await _initialize_tortoise_models(
        conf=DATABASE
    )


async def shutdown_event() -> None:
    if isinstance(_test, str):
        return await test_shutdown_event()


""" TEST MODE """


async def test_startup_event() -> None:
    """
    Test startup events such as initializing db, models...

    :return: None
    """

    if _database_to_use == 'sqlite':
        await _initialize_tortoise_models()
        return

    DATABASE: DatabaseConfig = DatabaseConfig(
        _testmode=True
    )

    await _delete_and_create_test_database(
        conf=DATABASE
    )

    await _initialize_tortoise_models(
        conf=DATABASE
    )


async def test_shutdown_event() -> None:
    await Tortoise.close_connections()


async def _delete_and_create_test_database(conf: DatabaseConfig) -> None:
    """
    Droping test database if exists and creating new.

    :param conf: Database configuration.
    :return:
    """

    _connection: Dict = {
        'user': conf.db_user,
        'password': conf.db_password,
        'host': conf.db_host,
        'port': conf.db_port,
        'database': 'template1'
    }

    try:
        _conn: asyncpg.connection.Connection = await asyncpg.connect(**_connection)
    except Exception:
        raise

    try:
        exists: int = await _conn.fetchval(
            'SELECT 1 FROM pg_database WHERE datname = $1',
            conf.db_name
        )

        if exists:
            await _conn.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = $1
                """,
                conf.db_name
            )

            await _conn.execute(
                f'DROP DATABASE {conf.db_name}'
            )

        else:
            raise ValueError('Unable to kill sessions or drop database!')

        await _conn.execute(
            f'CREATE DATABASE {conf.db_name}'
        )

    except Exception as e:
        raise

    finally:
        await _conn.close()


async def _initialize_tortoise_models(conf: Optional[DatabaseConfig] = None) -> None:
    """
    Initialize Tortoise ORM with the provided configuration.

    Args:
        conf (Dict): Configuration dictionary containing database connection details.
    """

    _url: AnyStr = f'sqlite://:memory:'
    if conf:
        _url: AnyStr = f'postgres://{conf.db_user}:{conf.db_password}@{conf.db_host}:{conf.db_port}/{conf.db_name}'

    try:
        await Tortoise.init(
            db_url=_url,
            modules={
                'models': ['models']
            }
        )

        await Tortoise.generate_schemas()
    except Exception:
        raise

    return


service: FastAPI = get_service()
