# Prefect Experiments

A series of experiments with [Prefect](https://github.com/prefecthq/prefect).

## Task and Flow contexts

Typically, Prefect tasks and flows are defined as Python functions, decorated with `@task` or `@flow`. This is great for most use cases and permits functionality such as retries by encapsulating the logic in a function that can be called multiple times. However, there are some cases where you might want to define a task or flow in a more dynamic way, such as when you want to wrap third-party code in a Prefect task or track execution without needing to abstract the logic into a function.

For these use cases, we introduce flow and task contexts. These contexts operate exactly like a decorated function: they create new task or flow runs when they are opened, transition into a running state while code inside the context executes, and finally complete or fail when the context is exited. The key difference is that the context is not a function, so certain functionality like retries are not available. 

```python
from prefect_experiments.task_context import task_context

with task_context(name='My print task'):
    # Any code inside this context will be executed as a Prefect task
    print("Hello, world!")
    print("Goodbye!")
```
 
## Pytest fixtures

One application of task and flow contexts is to wrap every unit test in a task context for observibility and tracking. To set this up, import all of the fixtures from `prefect_experiments.fixtures` into your `conftest.py` file. This repo's unit tests are set up this way.

```python
# conftest.py
from prefect_experiments.fixtures import *

# ... the rest of your conftest.py file
```
