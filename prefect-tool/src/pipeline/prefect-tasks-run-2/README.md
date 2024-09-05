## Set up
​
### Step 1: Activate a virtual environment

This example uses conda, but any virtual environment manager will work.

```bash
conda deactivate
conda create -n python-tasks python=3.12
conda activate python-tasks
```

### Step 2: Install Python dependencies

```bash
pip install -U prefect marvin fastapi==0.107
```


### Step 3: Connect to Prefect Cloud or a self-hosted Prefect server

Use either Prefect Cloud or a self-hosted Prefect server for these examples.

You must have PREFECT_API_URL set to send tasks to task workers.

If you’re using a Prefect server with a SQLite backing database (the default database), save this value to your active Prefect Profile with the following command:

```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

If using Prefect Cloud, set the PREFECT_API_URL value to the Prefect Cloud API URL and add your API key.

The examples that use docker (examples 4 and 5) use a Prefect server by default. You can switch to Prefect Cloud by changing the PREFECT_API_URL and adding a variable for your API key in the docker-compose.yaml. Or use a Prefect server backed by a PostgreSQL database by setting the PREFECT_API_DATABASE_CONNECTION_URL.

If using Prefect server instead of Prefect Cloud, start your server by running the following command:

```bash
prefect server start
```

## Example 1: Run a Prefect task in the foreground by calling it
Add the @task decorator to any Python function to define a Prefect task.

​
### Step 1: Create a file with a task-decorated function

Create a file named task.py and save the following code in it

```python
from prefect import task

@task(log_prints=True)
def greet(name: str = "Marvin"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet()

```

You should see the task run in the terminal. This task runs in the foreground, meaning it is not deferred.

You can see the task run in the UI. If you’re using a self-hosted Prefect server instance, you can also see the task runs in the database.

## Example 2: Start a task worker and run deferred tasks in the background

To run tasks in a separate process or container, start a task worker, similar to how you would run a Celery worker or an arq worker. The task worker continually receives scheduled tasks to execute from Prefect’s API, executes them, and reports the results back to the API. Run a task worker by passing tasks into the prefect.task_worker.serve() method.
​
### Step 1: Define the task and task worker in a file

```python
from prefect import task
from prefect.task_worker import serve


@task
def my_background_task(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    serve(my_background_task)
```

### Step 2: Start the task worker by running the script in the terminal

```python
python task_worker.py
```

The task worker is waiting for runs of the my_background_task task.

​
### Step 3: Create a file and save the following code in it:

task_scheduler.py
```python
from task_worker import my_background_task


if __name__ == "__main__":
    my_background_task.delay("Agrajag")
```

### Step 4: Open another terminal and run the script

```
python task_scheduler.py
```

Note that we return a "future" from the `delay` method. You can use this object to wait for the task to complete with `wait()` and to retrieve its result with `result()`.
We can also see the task run's UUID and other information about the task run.

Step 5: See the task run in the UI.

Open Prefect's UI and navigate to the Runs page. Select "Tasks" to see a list of task runs. You should see your new task in the list.

Step 6: You can use multiple task workers to run tasks in parallel.

Start another instance of the task worker. In another terminal run:

```bash
python task_worker.py
```

Step 7: Submit multiple tasks to the task worker.

Modify the `task_submitter.py` file to submit multiple tasks to the task worker with different inputs:

```python
from tasks import my_background_task

if __name__ == "__main__":
    my_background_task.delay("Ford")
    my_background_task.delay("Prefect")
    my_background_task.delay("Slartibartfast")
```

Run the file and watch the work get distributed across both task workers!

Step 8: Shut down the task servers with *control* + *c*.

Alright, you can submit tasks to multiple Prefect task workers running in the background!
This is cool because we can observe these tasks executing in parallel and very quickly with web sockets - no polling required.
