import asyncio
import datetime
import os
import sys
import json

from pathlib import Path

MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
sys.path.append(MODEL_PATH)


from tables import (
    database,
    movies,
    people,
    planets,
    species,
    starships,
)  # noqa


def _get_data(url):
    here = Path(__file__).parent

    with open(here / "cache.json") as f:
        cache = json.load(f)

    next_page = url

    results = []

    while next_page:
        data = cache[next_page]

        results += data["results"]
        next_page = data["next"]

    return results


def _get_id_from_url(url):
    parts = url.split('/')

    return parts[-2]


def _convert_datetime(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def _convert_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")


async def load_films(database):
    films = _get_data("https://swapi.co/api/films/")

    for film in films:
        await database.execute(
            query=movies.insert(),
            values={
                "title": film["title"],
                "director": film["director"],
                "producer": film["producer"],
                "episode_id": film["episode_id"],
                "release_date": _convert_date(film["release_date"]),
                "opening_crawl": film["opening_crawl"],
            },
        )


async def load_people(database):
    all_people = _get_data("https://swapi.co/api/people/")

    for person in all_people:
        await database.execute(
            query=people.insert(),
            values={
                "name": person["name"],
                "created": _convert_datetime(person["created"]),
                "edited": _convert_datetime(person["edited"]),
                "gender": person["gender"],
                "skin_color": person["skin_color"],
                "hair_color": person["hair_color"],
                "height": person["height"],
                "mass": (
                    float(person["mass"].replace(",", "."))
                    if person["mass"] != "unknown"
                    else None
                ),
                "eye_color": person["eye_color"],
                "birth_year": person["birth_year"],
                "homeworld_id": _get_id_from_url(person["homeworld"]),
            },
        )


async def load_planets(database):
    all_planets = _get_data("https://swapi.co/api/planets/")

    for planet in all_planets:
        await database.execute(
            query=planets.insert(),
            values={
                "name": planet["name"],
                "created": _convert_datetime(planet["created"]),
                "edited": _convert_datetime(planet["edited"]),
                "climate": planet["climate"],
                "terrain": planet["terrain"],
                "gravity": planet["gravity"],
                "surface_water": planet["surface_water"],
                "diameter": planet["diameter"],
                "rotation_period": planet["rotation_period"],
                "orbital_period": planet["orbital_period"],
                "population": planet["population"],
            },
        )


async def load_species(database):
    all_species = _get_data("https://swapi.co/api/species/")

    for specie in all_species:
        await database.execute(
            query=species.insert(),
            values={
                "name": specie["name"],
                "created": _convert_datetime(specie["created"]),
                "edited": _convert_datetime(specie["edited"]),
                "designation": specie["designation"],
                "eye_colors": specie["eye_colors"],
                "skin_colors": specie["skin_colors"],
                "hair_colors": specie["hair_colors"],
                "language": specie["language"],
                "average_lifespan": specie["average_lifespan"],
                "average_height": specie["average_height"],
            },
        )


async def load_starships(database):
    all_starships = _get_data("https://swapi.co/api/starships/")

    for starship in all_starships:
        await database.execute(
            query=starships.insert(),
            values={
                "name": starship["name"],
                "created": _convert_datetime(starship["created"]),
                "edited": _convert_datetime(starship["edited"]),
                "cost_in_credits": starship["cost_in_credits"],
                "length": starship["length"],
                "max_atmosphering_speed": starship["max_atmosphering_speed"],
                "crew": starship["crew"],
                "passengers": starship["passengers"],
                "cargo_capacity": starship["cargo_capacity"],
                "consumables": starship["consumables"],
                "hyperdrive_rating": starship["consumables"],
                "MGLT": starship["MGLT"],
                "starship_class": starship["starship_class"],
            },
        )


async def import_data():
    await database.connect()

    await database.execute(query=movies.delete())
    await database.execute(query=people.delete())
    await database.execute(query=planets.delete())
    await database.execute(query=species.delete())
    await database.execute(query=starships.delete())

    await load_films(database)
    await load_people(database)
    await load_planets(database)
    await load_species(database)
    await load_starships(database)


loop = asyncio.get_event_loop()
loop.run_until_complete(import_data())
loop.close()
