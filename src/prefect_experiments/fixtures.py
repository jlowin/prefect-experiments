from contextvars import copy_context

import pytest

from prefect_experiments.flow_context import flow_context
from prefect_experiments.task_context import task_context


def restore_context(context):
    """
    Pytest doesn't preserve contextvars across fixtures, so we need to yield the
    context from each parent fixture and restore it in the child fixture.
    """
    for var, value in context.items():
        var.set(value)


@pytest.fixture(autouse=True, scope="session")
async def context_for_session():
    async with flow_context("Unit Tests"):
        yield copy_context()


@pytest.fixture(autouse=True, scope="module")
async def context_for_module(request: pytest.FixtureRequest, context_for_session):
    restore_context(context_for_session)
    # with FlowRunContext(**context_for_session.dict()):
    async with flow_context(request.module.__name__):
        yield copy_context()


@pytest.fixture(autouse=True, scope="class")
async def context_for_class(request: pytest.FixtureRequest, context_for_module):
    restore_context(context_for_module)
    if request.cls is not None:
        async with flow_context(request.cls.__name__):
            yield copy_context()
    else:
        yield copy_context()


@pytest.fixture(autouse=True, scope="function")
async def context_for_test(request: pytest.FixtureRequest, context_for_class):
    restore_context(context_for_class)
    async with task_context(name=request.node.name):
        yield copy_context()
