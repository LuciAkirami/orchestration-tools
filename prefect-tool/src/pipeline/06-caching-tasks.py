import time
from datetime import timedelta

from prefect import flow, task
from prefect.tasks import task_input_hash

# --------------------------- Caching ------------------------
# Let's say there is a function, a pure function, that if you give the function the same
# input, it always produces the same output, for example
# def two_times_x(x: int) -> int:
#     time.sleep(2)
#     return x*2
# if the input is 4, it will always returns 8. Let's say the function is a bit complex and takes time to generate it
# so for better performance, what we can do is, cache the function, that is save the input and output as a hash,
# and if we get the same input, then check if its in the hash, and if it is, then directly return the output instead of
# running the func, whic will take time to generate the ans


# here, we pass task_input_hash to cache_key_fn which tells hash the input and if the same input is given to the function
# return the saved output for that input instead of passing it o the function
# cache_expiration tells how much time will this cache will live. So this cache expires after 1 hour. So after 1 hour,
# if we give the same input, then as the cache is expired, the input is sent to the function, it will then calculat the o/p and return it
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def two_times_x(x: int) -> int:
    time.sleep(
        5
    )  # assume its a time consuming task / an api call that will return same output for same input
    return x * 2


@flow
def test_caching(x: int):
    response = two_times_x(x)
    print(response)


if __name__ == "__main__":
    # run it for first time, it takes 5 seconds for o/p
    # then run it for second time, it will run instantaneously
    test_caching(10)
