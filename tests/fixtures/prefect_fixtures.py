import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import pytest
from prefect import Flow
from prefect.context import FlowRunContext, TaskRunContext
from prefect.new_flow_engine import FlowRun, FlowRunEngine
from prefect_experiments.flow_context import flow_context
from prefect_experiments.task_context import task_context


@pytest.fixture(autouse=True, scope="session")
async def flow_context_for_session():
    async with flow_context("Unit Tests"):
        yield FlowRunContext.get()


@pytest.fixture(autouse=True, scope="module")
async def flow_context_for_module(
    request: pytest.FixtureRequest,
    flow_context_for_session,
):
    with FlowRunContext(**flow_context_for_session.dict()):
        async with flow_context(request.module.__name__):
            yield FlowRunContext.get()


@pytest.fixture(autouse=True)
async def run_tests_as_tasks(
    request: pytest.FixtureRequest,
    flow_context_for_module,
):
    with FlowRunContext(**flow_context_for_module.dict()):
        async with task_context(name=request.node.name):
            yield
