from prefect import flow, task

# flows can be nested within each other


@task()
def flow2_task(log_prints=True):
    print("I'm a task executed by Flow 2")


@flow()
def nested_flow(log_prints=True):
    print("I'm a nested flow")
    flow2_task()


@task()
def flow1_task(log_prints=True):
    print("I'm a task executed by Flow 1")


@flow()
def main_flow(log_prints=True):
    flow1_task()
    # here i'm adding nested_flow. So now this flow becomes a subflow
    # Both subflows and flows are shown in the Flow Runs and Flow page ,
    # so you don't need to go inside the first flow to check the nested flow
    nested_flow()


if __name__ == "__main__":
    main_flow()
