from contextlib import contextmanager

import prefect.states

from prefect_experiments.task_context import task_context


@contextmanager
def step(name: str, description: str = None):
    """
    Convenient way to create a human-readable step in a flow.
    """
    with task_context(name=name, description=description, tags=["step"]):
        yield


def expectation(name: str, outcome: bool, description: str = None):
    if outcome not in {True, False, None}:  # pragma: no cover
        raise ValueError(
            f"Expectation outcome must be True, False, or None, not {outcome}."
        )
    with task_context(name=name, description=description, tags=["expectation"]) as run:
        if outcome is True:
            run.set_state(prefect.states.Completed(message="Expectation satisfied."))
        elif outcome is False:
            run.set_state(prefect.states.Failed(message="Expectation not satisfied."))
        elif outcome is None:
            run.set_state(
                prefect.states.Pending(message="Expectation not yet evaluated.")
            )
