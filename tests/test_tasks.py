from prefect import flow, task
from prefect_experiments.tasks import step


@task
def f(x):
    return x


@task
def add(x, y):
    return x + y


@task
def subtract(x, y):
    return x - y


class TestStep:
    def test_step(self):
        @flow
        def my_flow():
            with step("Step 1"):
                x = f(1)
                y = f(2)
            with step("Step 2"):
                z = add(x, y)
            return z

        assert my_flow()

    def test_nested_step(self):
        @flow
        def my_flow():
            with step("Step 1"):
                x = f(1)
                y = f(2)
                with step("Substep 1"):
                    z = add(x, y)
            return z

        assert my_flow()
