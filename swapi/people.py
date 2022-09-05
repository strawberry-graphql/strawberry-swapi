import typing

import strawberry

from tables import database, people, planets, starships
from utils import get_generic_connection

import prisma

from .node import Node
from .page_info import PageInfo
from .planets import Planet
from .starships import PersonStarshipsConnection, PersonStarshipsEdge


@strawberry.type
class Person(Node):
    name: typing.Optional[str]
    homeworld_id: strawberry.Private[int]
    # TODO: add these to the db
    created: typing.Optional[str] = None
    edited: typing.Optional[str] = None
    gender: typing.Optional[str] = None
    skin_color: typing.Optional[str] = None
    hair_color: typing.Optional[str] = None
    height: typing.Optional[int] = None
    mass: typing.Optional[float] = None
    eye_color: typing.Optional[str] = None
    birth_year: typing.Optional[str] = None

    starship_connection: typing.Optional[
        "PersonStarshipsConnection"
    ] = strawberry.field(
        resolver=get_generic_connection(
            starships, PersonStarshipsConnection, PersonStarshipsEdge
        )
    )

    @strawberry.field
    async def homeworld(self, info) -> typing.Optional[Planet]:
        query = planets.select().where(planets.c.id == self.homeworld_id)

        row = await database.fetch_one(query=query)

        if not row:
            print(self.homeworld_id)
            return None

        return Planet.from_row(row)

    @staticmethod
    def from_row(row: prisma.models.people):
        return Person(
            id=row.id,
            name=row.name,
            homeworld_id=row.homeworld_id,
            gender=row.gender,
            skin_color=row.skin_color,
            hair_color=row.hair_color,
            height=row.height,
            mass=row.mass,
            eye_color=row.eye_color,
            birth_year=row.birth_year,
            # created=row.created,
            # edited=row.edited,
        )


@strawberry.type
class PeopleEdge:
    node: typing.Optional[Person]
    cursor: str

    @staticmethod
    def from_row(row):
        id_ = row[people.c.id]

        return PeopleEdge(cursor=id_, node=Person.from_row(row))


@strawberry.type
class PeopleConnection:
    page_info: PageInfo
    edges: typing.List[PeopleEdge]
    total_count: int
    people: typing.List[Person] = None
