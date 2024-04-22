import asyncio

import pytest

from .fixtures import *


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
def anyio_backend():
    """
    We can't use pytest-asyncio because it runs fixture setup and teardown in
    separate asyncio tasks, which breaks Prefect's Context reset() calls because
    the reset token comes from a different context.

    Anyio doesn't have that issue.
    """
    return "asyncio"
