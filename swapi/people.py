import typing

import prisma
import strawberry
from strawberry.types.info import Info
from utils import get_generic_connection

from .context import Context
from .node import Node
from .page_info import PageInfo
from .planets import Planet
from .starships import PersonStarshipsConnection, PersonStarshipsEdge


@strawberry.type
class Person(Node):
    name: str | None
    homeworld_id: strawberry.Private[int]
    # TODO: add these to the db
    created: str | None = None
    edited: str | None = None
    gender: str | None = None
    skin_color: str | None = None
    hair_color: str | None = None
    height: typing.Optional[int] = None
    mass: typing.Optional[float] = None
    eye_color: str | None = None
    birth_year: str | None = None

    starship_connection: PersonStarshipsConnection | None = strawberry.field(
        resolver=get_generic_connection(
            "starship", PersonStarshipsConnection, PersonStarshipsEdge
        )
    )

    @strawberry.field
    async def homeworld(self, info: Info[Context, None]) -> Planet | None:
        db = info.context["db"]

        planet = await db.planet.find_first(where={"id": self.homeworld_id})

        return Planet.from_row(planet) if planet is not None else None

    @staticmethod
    def from_row(row: prisma.models.people):
        return Person(
            id=strawberry.ID(str(row.id)),
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
    def from_row(row: prisma.models.people):
        return PeopleEdge(cursor=str(row.id), node=Person.from_row(row))


@strawberry.type
class PeopleConnection:
    page_info: PageInfo
    edges: typing.List[PeopleEdge]
    total_count: int
    people: typing.List[Person] = None
