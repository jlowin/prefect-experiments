import pytest
from prefect_experiments.flow_context import flow_context


async def test_empty_context():
    async with flow_context("test") as run:
        assert run.state.is_running()
    assert run.state.is_completed()


async def test_context_with_code():
    async with flow_context("a collection of functions") as run:
        x = sum([1, 2, 3, 4])
    assert x == 10
    assert run.state.is_completed()


async def test_error_context():
    with pytest.raises(ValueError, match="test error"):
        async with flow_context("test") as run:
            assert run.state.is_running()
            raise ValueError("test error")
    assert run.state.is_failed()


async def test_context_name():
    async with flow_context("test") as run:
        pass
    assert run.flow_run.name == "test"


async def test_context_passing_retry_raises_errors():
    with pytest.raises(
        ValueError, match="Unsupported keyword arguments for a flow context provided"
    ):
        async with flow_context("test", max_retries=1):
            pass
