from contextlib import asynccontextmanager
from typing import AsyncIterator

from prefect import Flow
from prefect.new_flow_engine import FlowRun, FlowRunEngine


@asynccontextmanager
async def flow_context(
    name: str, parameters: dict = None, **flow_kwargs
) -> AsyncIterator[FlowRun]:
    """
    Create a flow context for running functions inside a Prefect flow.

    This is useful for running arbitrary code or third party libraries as a
    Prefect flow without having to define a new function.

    Example:
    ```python
    async with flow_context("Running library..."):
        x = do_stuff()
        y = do_more_stuff(x)
        z = do_even_more_stuff(y)
    ```
    """
    supported_kwargs = {
        "name",
        "description",
        "tags",
        "version",
    }
    unsupported_kwargs = set(flow_kwargs.keys()) - set(supported_kwargs)
    if unsupported_kwargs:
        raise ValueError(
            f"Unsupported keyword arguments for a flow context provided: "
            f"{unsupported_kwargs}. Consider using a @flow-decorated function instead."
        )

    flow = Flow(name=name, fn=lambda: None, flow_run_name=name, **flow_kwargs)
    engine = FlowRunEngine(flow=flow, parameters=parameters)
    async with engine.start() as run:
        await run.begin_run()
        try:
            yield run
            await run.handle_success(result=None)
            return
        except Exception as exc:
            await run.handle_exception(exc)
            raise
