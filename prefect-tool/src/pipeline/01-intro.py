import httpx
from prefect import flow, task
from rich import print
from rich.pretty import pprint


# a task is a atomic unit of work which is run by a task runner
# by deafult the name of the task is name of the func
@task(name="Get Stats", description="Gets the stats for a Pokemon")
def get_stats(pokemon_info: str):
    stats = pokemon_info["stats"]

    # to view the stats dict
    print(stats)

    return {
        "hp": stats[0]["base_stat"],
        "attack": stats[1]["base_stat"],
        "defence": stats[1]["base_stat"],
    }


# Flows are defined as Python functions. They can take inputs, perform work, and return a result.
# Flows can contain one / multiple tasks. The default name of the flow is name of the function
# you can even give custom names, description and versions which is optional
@flow(name="Pokemon Info Getter", description="Gets the information about a pokemon")
def get_pokemon_info(base_url: str, pokemon: str):
    """Fetch information about a Pokemon"""
    url = f"{base_url}/pokemon/{pokemon}"

    api_response = httpx.get(url)
    pokemon_info = api_response.json()

    stats_response = get_stats(pokemon_info)

    print("Pokemon Stats\n")
    pprint(stats_response, expand_all=True)


if __name__ == "__main__":
    # Flow Run - A flow run is a single execution of a flow.
    # try giving a dictionary instead of string for pokemon
    # if you do the above, the flow will stop as it does type validation and coercion to make sure
    # inputs are of right types
    get_pokemon_info(base_url="https://pokeapi.co/api/v2/", pokemon="pikachu")

# we can ruyn flows directly by running the python script, or through cron jobs and deployments
