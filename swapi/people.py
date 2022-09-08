import prisma
import strawberry
from strawberry.types.info import Info

from swapi.utils.datetime import format_datetime

from .context import Context
from .node import Node
from .page_info import PageInfo
from .planets import Planet


@strawberry.type
class Person(Node):
    name: str | None
    homeworld_id: strawberry.Private[int]
    created: str | None = None
    edited: str | None = None
    gender: str | None = None
    skin_color: str | None = None
    hair_color: str | None = None
    height: int | None = None
    mass: float | None = None
    eye_color: str | None = None
    birth_year: str | None = None

    # starship_connection: PersonStarshipsConnection | None = strawberry.field(
    #     resolver=get_generic_connection(
    #         "starship", PersonStarshipsConnection, PersonStarshipsEdge
    #     )
    # )

    @strawberry.field
    async def homeworld(self, info: Info[Context, None]) -> Planet | None:
        from .planets import Planet

        db = info.context["db"]

        planet = await db.planet.find_first(where={"id": self.homeworld_id})

        return Planet.from_row(planet) if planet is not None else None

    @staticmethod
    def from_row(row: prisma.models.Person):
        return Person(
            id=strawberry.ID(Node.get_global_id("people", row.id)),
            name=row.name,
            homeworld_id=row.homeworld_id,
            gender=row.gender,
            skin_color=row.skin_color,
            hair_color=row.hair_color,
            height=row.height,
            mass=row.mass,
            eye_color=row.eye_color,
            birth_year=row.birth_year,
            created=format_datetime(row.created),
            edited=format_datetime(row.edited),
        )


@strawberry.type
class PeopleEdge:
    node: Person | None
    cursor: str


@strawberry.type
class PeopleConnection:
    page_info: PageInfo
    edges: list[PeopleEdge]
    total_count: int
    people: list[Person]
