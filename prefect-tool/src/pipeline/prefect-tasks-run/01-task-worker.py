from prefect import task
from prefect.task_worker import serve

# --------------------- Deferred Tasks ---------------------------------
# Prefect tasks are Python functions that can be run immediately or deferred for background execution.
# Deferred Prefect tasks run in a background process using a Prefect task worker.
# Use deferred tasks to move work out of the foreground of your application and
# distribute concurrent execution across multiple processes or machines.

# --Example
# For example, if you have a web application, deferred tasks allow you to offload processes
# such as sending emails, processing images, or inserting data into a database.

# For more info, check https://docs.prefect.io/3.0/develop/deferred-tasks#defining-a-task

# -------- Executing deferred tasks with a task worker ------
# To run tasks in a separate process or container, start a task worker.
# The task worker continually receives instructions to execute deferred tasks from Prefect’s API, executes them,
# and reports the results back to the API.


@task
def my_background_task(name: str):
    # Task logic here
    print(f"Hello, {name}!")


if __name__ == "__main__":
    # Run a task worker by passing tasks into the prefect.task_worker.serve() method:
    # NOTE: The serve() function accepts multiple tasks. The Task worker
    # will listen for scheduled task runs for all tasks passed in.
    serve(my_background_task)
    # NOTE: Task workers only run deferred tasks, not tasks you call directly as normal Python functions.

# To run this, you can either directly run the file or do the following in CLI
# prefect task serve 01-task-worker.py:my_background_task
# Running this will start a task worker

# Run this, check the cli
#  then go to 02-call-deferred-task.py, run the .delay() in another cli and observe the output in the above cli

# So running this py file starts a long-lived process that listens for scheduled runs of these tasks, here it listens
# for my_background_task(), and when we run the 02 file, this process will execute the func instead of the 02 file
