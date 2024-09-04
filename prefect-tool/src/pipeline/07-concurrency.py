import time
from datetime import timedelta

from prefect import flow, task
from prefect.tasks import task_input_hash


# commenting the below line, as we want to see how synchronous and concurrency works
# @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=2))
@task
def fetching_from_api(x: int):
    time.sleep(2)
    return x


# in this typical execution, tasks run synchronously
@flow
def execute_tasks_synchronously():
    res = []
    for i in range(1, 10):
        res.append(fetching_from_api(i))
        # here we are calling the task 10 times, and as it runs synchronously bydefault
        # it will take 10*2 = 20 seconds to finish
    return res


# ------------------------- Running Tasks Concurrently -------------------------------
# Tasks enable concurrent execution, allowing you to execute multiple tasks asynchronously.
# This concurrency can greatly enhance the efficiency and performance of your workflows.

# Now you’re fetching the data you need from fetching_from_api(), but the requests happen sequentially.
# Tasks expose a submit method that changes the execution from sequential to concurrent.
# In this example, you also need to use the result method to unpack a list of return values:


@flow
def execute_tasks_concurrently():
    res = []
    for i in range(1, 10):
        # here instead of fetching_from_api(i), we do fetching_from_api.submit(i), which lets tasks run concurrently
        res.append(fetching_from_api.submit(i))

    # finally we need to call the .result() for each task to obtain the values returned from that task
    res = [individual_result.result() for individual_result in res]
    return res


if __name__ == "__main__":
    # run this while commenting execute_tasks_concurrently() and check how much time it takes
    # execute_tasks_synchronously()
    # run this while commenting execute_tasks_synchronously and check how much time it takes
    execute_tasks_concurrently()
    # Check the Flow Runs for both Flows in the server to see how the tasks are executed
