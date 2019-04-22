import requests

from graphql.utilities.introspection_query import get_introspection_query


def get_schema(url: str) -> dict:
    query = get_introspection_query()

    response = requests.post(url, json={"query": query})

    return response.json()["data"]["__schema"]


def do_diff(local_schema, remote_schema):
    # kinds = [
    #     "directives",
    #     "types",
    # ]

    local_directives = {
        directive["name"] for directive in local_schema["directives"]
    }
    remote_directives = {
        directive["name"] for directive in remote_schema["directives"]
    }

    missing_directives = remote_directives - local_directives

    if missing_directives:
        print(f"Missing directives: {missing_directives}")

    local_types = {type_["name"] for type_ in local_schema["types"]}
    remote_types = {type_["name"] for type_ in remote_schema["types"]}

    missing_types = remote_types - local_types

    if missing_types:
        print(f"Missing types: {missing_types}")


if __name__ == "__main__":
    print("Downloading local schema, make sure server is app")

    local_schema = get_schema("http://localhost:8000/graphql")

    print("Downloading remote schema")

    remote_schema = get_schema("http://localhost:61010")

    do_diff(local_schema, remote_schema)

    remote_schema
