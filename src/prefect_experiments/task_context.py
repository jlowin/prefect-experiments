from contextlib import asynccontextmanager
from typing import AsyncIterator

from prefect import Task
from prefect.new_task_engine import TaskRun, TaskRunEngine, timeout


@asynccontextmanager
async def task_context(
    name: str, parameters: dict = None, **task_kwargs
) -> AsyncIterator[TaskRun]:
    """
    Create a task context for running functions inside a Prefect task.

    This is useful for running arbitrary code or third party libraries as a
    Prefect task without having to define a new function. The runtime of the task
    is controlled by the task context.

    Example:
    ```python
    async with task_context("Running library..."):
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
        "timeout_seconds",
        "log_prints",
        "on_completion",
        "on_failure",
        "viz_return_value",
    }
    unsupported_kwargs = set(task_kwargs.keys()) - set(supported_kwargs)
    if unsupported_kwargs:
        raise ValueError(
            f"Unsupported keyword arguments for a task context provided: "
            f"{unsupported_kwargs}. Consider using a @task-decorated function instead."
        )

    task = Task(name=name, fn=lambda: None, task_run_name=name, **task_kwargs)
    engine = TaskRunEngine(task=task, parameters=parameters)
    async with engine.start() as run:
        await run.begin_run()
        async with run.enter_run_context():
            try:
                async with timeout(run.task.timeout_seconds):
                    yield run
                    await run.handle_success(result=None)
                    return
            except Exception as exc:
                await run.handle_exception(exc)
                raise
