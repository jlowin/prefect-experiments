import pytest
from prefect.context import FlowRunContext

from prefect_experiments.flow_context import flow_context
from prefect_experiments.task_context import task_context


@pytest.fixture(autouse=True, scope="session")
async def context_for_session():
    async with flow_context("Unit Tests"):
        yield FlowRunContext.get()


@pytest.fixture(autouse=True, scope="module")
async def context_for_module(
    request: pytest.FixtureRequest,
    context_for_session,
):
    # open this manually because fixtures aren't necessarily run in the same frame
    # so the parent flow/task contexts may not be visible to the child fixture
    # this is due to a unique pytest behavior
    with FlowRunContext(**context_for_session.dict()):
        async with flow_context(request.module.__name__):
            yield FlowRunContext.get()


@pytest.fixture(autouse=True, scope="class")
async def context_for_class(
    request: pytest.FixtureRequest,
    context_for_module,
):
    # open this manually because fixtures aren't necessarily run in the same frame
    # so the parent flow/task contexts may not be visible to the child fixture
    # this is due to a unique pytest behavior
    with FlowRunContext(**context_for_module.dict()):
        if request.cls is not None:
            async with flow_context(request.cls.__name__):
                yield FlowRunContext.get()
        else:
            yield FlowRunContext.get()


@pytest.fixture(autouse=True, scope="function")
async def context_for_test(
    request: pytest.FixtureRequest,
    context_for_class,
):
    # open this manually because fixtures aren't necessarily run in the same frame
    # so the parent flow/task contexts may not be visible to the child fixture
    # this is due to a unique pytest behavior
    with FlowRunContext(**context_for_class.dict()):
        async with task_context(name=request.node.name):
            yield
