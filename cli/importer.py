import json
from base64 import b64decode
from dataclasses import dataclass

import prisma
from dateutil import parser

from .constants import (
    FILMS_QUERY,
    PEOPLE_QUERY,
    PLANETS_QUERY,
    REFERENCE_API_URL,
    SPECIES_QUERY,
    VEHICLES_QUERY,
    STARSHIP_QUERY,
)
from .utils.query import query


@dataclass
class Importer:
    db: prisma.Prisma

    async def _load_people(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            PEOPLE_QUERY.read_text(),
        )

        people = response["data"]["allPeople"]["people"]

        for person in people:
            await self.db.person.create(
                data={
                    "id": self._parse_id(person["id"]),
                    "name": person["name"],
                    "birth_year": person["birthYear"],
                    "eye_color": person["eyeColor"],
                    "gender": person["gender"],
                    "hair_color": person["hairColor"],
                    "height": person["height"],
                    "mass": person["mass"],
                    "homeworld_id": self._parse_id(person["homeworld"]["id"]),
                    "skin_color": person["skinColor"],
                    "created": parser.isoparse(person["created"]),
                    "edited": parser.isoparse(person["edited"]),
                    "species_id": (
                        self._parse_id(person["species"]["id"])
                        if person["species"]
                        else None
                    ),
                    "films": {
                        "connect": [
                            {"id": self._parse_id(film["id"])}
                            for film in person["filmConnection"]["films"]
                        ]
                    },
                    "starships": {
                        "connect": [
                            {"id": self._parse_id(starship["id"])}
                            for starship in person["starshipConnection"]["starships"]
                        ]
                    },
                    "vehicles": {
                        "connect": [
                            {"id": self._parse_id(vehicle["id"])}
                            for vehicle in person["vehicleConnection"]["vehicles"]
                        ]
                    },
                }
            )

    async def _load_films(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            FILMS_QUERY.read_text(),
        )

        films = response["data"]["allFilms"]["films"]

        # create many is not supported by sqlite

        for film in films:
            await self.db.film.create(
                data={
                    "id": self._parse_id(film["id"]),
                    "title": film["title"],
                    "episode_id": film["episodeID"],
                    "opening_crawl": film["openingCrawl"],
                    "director": film["director"],
                    "producers": json.dumps(film["producers"]),
                    "release_date": parser.isoparse(film["releaseDate"]),
                    "created": parser.isoparse(film["created"]),
                    "edited": parser.isoparse(film["edited"]),
                    "species": {
                        "connect": [
                            {"id": self._parse_id(specie["id"])}
                            for specie in film["speciesConnection"]["species"]
                        ]
                    },
                    "starships": {
                        "connect": [
                            {"id": self._parse_id(starship["id"])}
                            for starship in film["starshipConnection"]["starships"]
                        ]
                    },
                    "vehicles": {
                        "connect": [
                            {"id": self._parse_id(vehicle["id"])}
                            for vehicle in film["vehicleConnection"]["vehicles"]
                        ]
                    },
                    # "planets": {
                    #     "connect": [
                    #         {"id": self._parse_id(planet["id"])}
                    #         for planet in film["planetConnection"]["planets"]
                    #     ]
                    # },
                    # "characters": {
                    #     "connect": [
                    #         {"id": self._parse_id(character["id"])}
                    #         for character in film["characterConnection"]["characters"]
                    #     ]
                    # },
                }
            )

    async def _load_planets(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            PLANETS_QUERY.read_text(),
        )

        planets = response["data"]["allPlanets"]["planets"]

        for planet in planets:
            await self.db.planet.create(
                data={
                    "id": self._parse_id(planet["id"]),
                    "name": planet["name"],
                    "rotation_period": planet["rotationPeriod"],
                    "orbital_period": planet["orbitalPeriod"],
                    "diameter": planet["diameter"],
                    "climates": json.dumps(planet["climates"] or []),
                    "gravity": planet["gravity"],
                    "terrains": json.dumps(planet["terrains"] or []),
                    "surface_water": planet["surfaceWater"],
                    "population": planet["population"],
                    "created": parser.isoparse(planet["created"]),
                    "edited": parser.isoparse(planet["edited"]),
                }
            )

    async def _load_species(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            SPECIES_QUERY.read_text(),
        )

        species = response["data"]["allSpecies"]["species"]

        for specie in species:
            await self.db.species.create(
                data={
                    "id": self._parse_id(specie["id"]),
                    "name": specie["name"],
                    "classification": specie["classification"],
                    "designation": specie["designation"],
                    "average_height": specie["averageHeight"],
                    "average_lifespan": specie["averageLifespan"],
                    "eye_colors": json.dumps(specie["eyeColors"] or []),
                    "hair_colors": json.dumps(specie["hairColors"] or []),
                    "skin_colors": json.dumps(specie["skinColors"] or []),
                    "language": specie["language"],
                    "created": parser.isoparse(specie["created"]),
                    "edited": parser.isoparse(specie["edited"]),
                }
            )

    async def _load_vehicles(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            VEHICLES_QUERY.read_text(),
        )

        vehicles = response["data"]["allVehicles"]["vehicles"]

        for vehicle in vehicles:
            await self.db.vehicle.create(
                data={
                    "id": self._parse_id(vehicle["id"]),
                    "name": vehicle["name"],
                    "model": vehicle["model"],
                    "vehicle_class": vehicle["vehicleClass"],
                    "manufacturers": json.dumps(vehicle["manufacturers"]),
                    "length": vehicle["length"],
                    "cost_in_credits": vehicle["costInCredits"],
                    "crew": vehicle["crew"],
                    "passengers": vehicle["passengers"],
                    "max_atmosphering_speed": vehicle["maxAtmospheringSpeed"],
                    "cargo_capacity": vehicle["cargoCapacity"],
                    "consumables": vehicle["consumables"],
                    "created": parser.isoparse(vehicle["created"]),
                    "edited": parser.isoparse(vehicle["edited"]),
                }
            )

    async def _load_starships(self) -> None:
        response = await query(
            REFERENCE_API_URL,
            STARSHIP_QUERY.read_text(),
        )

        starships = response["data"]["allStarships"]["starships"]

        for starship in starships:
            await self.db.starship.create(
                data={
                    "id": self._parse_id(starship["id"]),
                    "name": starship["name"],
                    "model": starship["model"],
                    "starship_class": starship["starshipClass"],
                    "manufacturers": json.dumps(starship["manufacturers"]),
                    "length": starship["length"],
                    "cost_in_credits": starship["costInCredits"],
                    "crew": starship["crew"],
                    "passengers": starship["passengers"],
                    "max_atmosphering_speed": starship["maxAtmospheringSpeed"],
                    "hyperdrive_rating": starship["hyperdriveRating"],
                    "MGLT": starship["MGLT"],
                    "cargo_capacity": starship["cargoCapacity"],
                    "consumables": starship["consumables"],
                    "created": parser.isoparse(starship["created"]),
                    "edited": parser.isoparse(starship["edited"]),
                }
            )

    async def import_all(self) -> None:
        await self.db.person.delete_many()
        await self.db.planet.delete_many()
        await self.db.species.delete_many()
        await self.db.film.delete_many()
        await self.db.vehicle.delete_many()
        await self.db.starship.delete_many()

        await self._load_planets()
        await self._load_starships()
        await self._load_species()
        await self._load_vehicles()
        await self._load_films()
        await self._load_people()

    @staticmethod
    def _parse_id(global_id: str) -> int:
        return int(b64decode(global_id).split(b":")[1])
