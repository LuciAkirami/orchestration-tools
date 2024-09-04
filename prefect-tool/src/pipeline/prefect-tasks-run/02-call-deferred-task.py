# We are using importlib because
# from 01-deferred-tasks import my_background_task does not work
# as python import should not start with digits

import importlib

deferred_module = importlib.import_module("01-task-worker")

# run the task immediately
# deferred_module.my_background_task("Joaquim")

# Schedule the task for execution outside of this process
deferred_module.my_background_task.delay("Agrajg")

# so when u run the delay function, the taskworker created from the 01-task-worker.py will take care of
# executing the my_background_task() function
