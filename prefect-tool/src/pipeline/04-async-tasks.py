import asyncio

from prefect import flow, task

#  ---------- Task Execution ---------
# Tasks are always executed in the main thread by default, unless a specific
# task runner is used to execute them on different threads, processes, or infrastructure.
# This facilitates native Python debugging and profiling.

# ----------- Task Updates ---------
# Task updates are logged in batch, leading to eventual consistency for task states in the UI
# and API queries. While this means there may be a slight delay in seeing the most up-to-date task states,
# it allows for substantial performance improvements and increased workflow scale.

# ----------- Asynchronous Functions -----------
# Prefect also supports asynchronous Python functions.
# The resulting tasks are coroutines that can be awaited or run concurrently,


@task(log_prints=True)
async def print_values(values):
    for value in values:
        await asyncio.sleep(1)
        print(value, end=" ")


@flow(log_prints=True)
async def async_flow():
    print("Hello, I'm an async flow")

    # runs immediately
    await print_values([1, 2])

    # runs concurrently
    coros = [print_values("abcd"), print_values("6789")]
    await asyncio.gather(*coros)


if __name__ == "__main__":
    # check the logs to see how they are printed
    asyncio.run(async_flow())
