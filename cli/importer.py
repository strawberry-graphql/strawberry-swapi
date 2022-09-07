from base64 import b64decode
from dataclasses import dataclass

import prisma
from dateutil import parser

from .constants import FILMS_QUERY, PEOPLE_QUERY, REFERENCE_API_URL
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
                    "producers": ",".join(film["producers"]),
                    "release_date": parser.isoparse(film["releaseDate"]),
                    "created": parser.isoparse(film["created"]),
                    "edited": parser.isoparse(film["edited"]),
                }
            )

    async def import_all(self) -> None:
        await self.db.film.delete_many()
        await self.db.person.delete_many()

        await self._load_films()
        await self._load_people()

    @staticmethod
    def _parse_id(global_id: str) -> int:
        return int(b64decode(global_id).split(b":")[1])
