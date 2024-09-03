import time

import httpx
from prefect import flow, task


# ----------------- Timeout --------------------
# Task timeouts prevent unintentional long-running tasks. When the duration of execution
# for a task exceeds the duration specified in the timeout, a timeout exception is raised and the task is
# marked as failed. In the UI, the task is visibly designated as TimedOut
@task(timeout_seconds=1, log_prints=True)
def show_timeouts():
    print("I will execute")
    # it will fail here as max timeout is 1 second and we are sleeping for 5 seconds
    time.sleep(5)
    print("I will not execute")


@flow
def run_time_out_function():
    show_timeouts()


# ---------------------- Retries ---------------------
# Prefect can automatically retry task runs on failure. A task run fails if its Python function raises an exception.
# To enable retries, pass retries and retry_delay_seconds arguments to your task. If the task run fails,
# Prefect will retry it up to retries times, waiting retry_delay_seconds seconds between each attempt.
# If the task fails on the final retry, Prefect marks the task as failed.
@task(retries=2, retry_delay_seconds=5)
def get_data_task(url: str = "https://api.brittle-service.com/endpoint") -> dict:
    response = httpx.get(url)

    # If the response status code is anything but a 2xx, httpx will raise
    # an exception. This task doesn't handle the exception, so Prefect will
    # catch the exception and will consider the task run failed.
    response.raise_for_status()

    return response.json()


@flow
def get_data_flow():
    get_data_task()


# --------------- Retry Condition Function -------------------
# this function returns a true or false based on different HTTP STATUS Codes returned by the http.get()
# function. For certain STATUS Codes, this func will return a true and this true indicates that the
# task can perform retry and if this func  returns False, then task will fail and no retry performed
def retry_handler(task, task_run, state) -> bool:
    """Custom retry handler that specifies when to retry a task"""
    # print(task) # <prefect.tasks.Task object at 0x75154aeca3c0> object
    # print(type(task_run)) # <class 'prefect.client.schemas.objects.TaskRun'>
    # print(task_run.name) # my_api_call_task-0
    try:
        # Attempt to get the result of the task
        state.result()
    except httpx.HTTPStatusError as exc:
        # Retry on any HTTP status code that is not 401 or 404
        do_not_retry_on_these_codes = [401, 404]
        return exc.response.status_code not in do_not_retry_on_these_codes
    except httpx.ConnectError:
        # Do not retry
        return False
    except:
        # For any other exception, retry
        return True


# here we give the retry_handler func to the retry_condition_fn, which will decode if a retry is performed or not
@task(retries=1, retry_condition_fn=retry_handler)
def my_api_call_task(url):
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()


@flow
def get_data_flow_conditional_retry(url):
    my_api_call_task(url=url)


if __name__ == "__main__":
    # run_time_out_function()
    # comment the above function to try the retry flow, else above flow will fail and it will never move
    # to the retry flow
    # get_data_flow()
    # It will try two times with a 5 second gap between retries and fail

    # comment above two flows when trying to run the below flow, as above two fails will fail and this below flow wont run
    # get_data_flow_conditional_retry(url="https://httpbin.org/status/503") # performs a retry

    # comment above conditonal_retry_flow when using the below conditonal retry flow
    get_data_flow_conditional_retry(
        url="https://httpbin.org/status/404"
    )  # doesnt perform a retry


# ---------------- CUSTOM RETRY ------------------
# @task(retries=3, retry_delay_seconds=[1, 10, 100])
# when task fails, it waits for 1 second for the first retry and when 1st retry fails
# it will wait for 10 seconds for the 2nd retry and when 2nd retry fails, it will wait for
# 100seconds for the 3rd retry and when 3rd retry fails, the task will fail and so the flow

# ------------------- CONFIGURE RETRY GLOBALLY -------------------------
# prefect config set PREFECT_TASK_DEFAULT_RETRIES=2
# prefect config set PREFECT_TASK_DEFAULT_RETRY_DELAY_SECONDS = [1, 10, 100]


# ------------------- Thundering Herds Issue --------------------------

# Add “jitter” to avoid thundering herds
# You can add jitter to retry delay times. Jitter is a random amount of time added to retry periods
# that helps prevent “thundering herd” scenarios, which is when many tasks retry at the same time, potentially overwhelming systems.

# The retry_jitter_factor option can be used to add variance to the base delay. For example, a retry delay of
# 10 seconds with a retry_jitter_factor of 0.5 will allow a delay up to 15 seconds. Large values of retry_jitter_factor
# provide more protection against “thundering herds,” while keeping the average retry delay time constant. For example, the
# following task adds jitter to its exponential backoff so the retry delays will vary up to a maximum delay time of 20, 40,
# and 80 seconds respectively.

# from prefect import task
# from prefect.tasks import exponential_backoff


# @task(
#     retries=3,
#      # An exponential_backoff utility that will automatically generate a list of retry delays that correspond
#      # to an exponential backoff retry strategy. The following flow will wait for 10, 20, then 40 seconds before each retry.
#     retry_delay_seconds=exponential_backoff(backoff_factor=10),
#     retry_jitter_factor=1,
# )


# def some_task_with_exponential_backoff_retries():
#    (rest of code follows)
