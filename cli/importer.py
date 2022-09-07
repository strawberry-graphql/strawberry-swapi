import json
from base64 import b64decode
from dataclasses import dataclass

import prisma
from dateutil import parser

from .constants import (FILMS_QUERY, PEOPLE_QUERY, PLANETS_QUERY,
                        REFERENCE_API_URL, SPECIES_QUERY)
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
                    "skin_color": person["skinColor"],
                    "created": parser.isoparse(person["created"]),
                    "edited": parser.isoparse(person["edited"]),
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

    async def import_all(self) -> None:
        await self.db.film.delete_many()
        await self.db.person.delete_many()
        await self.db.planet.delete_many()
        await self.db.species.delete_many()

        await self._load_films()
        await self._load_people()
        await self._load_planets()
        await self._load_species()

    @staticmethod
    def _parse_id(global_id: str) -> int:
        return int(b64decode(global_id).split(b":")[1])
