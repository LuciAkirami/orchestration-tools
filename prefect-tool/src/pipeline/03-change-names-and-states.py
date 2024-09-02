import datetime

from prefect import flow, task
from prefect.runtime import flow_run
from prefect.states import Completed


# we can change the flow run names based on the input they recieve
# for this, we use the flow_run_name. This creates a unique run name for the flow
# and it changes based on the day you run it
@flow(flow_run_name="my-flow ran on {date:%A}")
def my_flow(date: datetime.datetime):
    # "A" pulls the day from the date
    print(f"Today is {date:%A}")


# If you need access to information about the flow, use the prefect.runtime module. For example:
def get_flow_params_and_generate_name():
    # get the name of the flow
    flow_name = flow_run.flow_name

    # get the parameters passed to the flow
    parameters = flow_run.parameters
    name = parameters["name"]
    limit = parameters["number"]

    # create a unique flow run name based on parameters
    return f"{flow_name}-with-{name}-and-{limit}"


# we can pass functions to flow_run_name
@flow(flow_run_name=get_flow_params_and_generate_name)
def my_second_flow(name: str, number: int):
    print(f"{name} gave me a number {number}")


# By default. when a flow finishes, it returns a completed state
# for example. the above two flows return "Finished in state Completed()"
# If a flow is failed, it returns a Failed() state. For More info on states: https://docs-3.prefect.io/3.0rc/develop/write-flows#final-state-determination
# a state is the final output returned by the flow
@flow
def my_third_flow(work_to_do: bool):
    if not work_to_do:
        # we can change the name of the state from Completed to Skipped with the name variable
        return Completed(message="No work to do 💤", name="Skipped")
    else:
        return Completed(message="Work was done 💪")


if __name__ == "__main__":
    # check UI to see the new flow run names for both the flows
    my_flow(datetime.datetime.now())
    my_second_flow(name="Luci", number=89)
    # Check the Logs - You will find "Finished in state Skipped("No work to do 💤")"
    my_third_flow(False)
    # Check the Logs - You will find "Finished in state Completed(message="Work was done 💪")"
    my_third_flow(True)
