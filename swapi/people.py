import prisma
from swapi.utils.datetime import format_datetime

import strawberry
from strawberry.types.info import Info

from .context import Context
from .film import Film, FilmsEdge
from .node import Node
from .page_info import PageInfo
from .planets import Planet
from .species import Species
from .starships import Starship, StarshipsEdge
from .utils.connections import get_connection_resolver
from .vehicles import Vehicle, VehiclesEdge


@strawberry.type
class PersonFilmsEdge(FilmsEdge): ...


@strawberry.type
class PersonFilmsConnection:
    page_info: PageInfo
    edges: list[PersonFilmsEdge | None] | None
    total_count: int | None
    films: list[Film | None] | None


@strawberry.type
class PersonStarshipsEdge(StarshipsEdge): ...


@strawberry.type
class PersonStarshipsConnection:
    page_info: PageInfo
    edges: list[PersonStarshipsEdge | None] | None
    total_count: int | None
    starships: list[Starship | None] | None


@strawberry.type
class PersonVehiclesEdge(VehiclesEdge): ...


@strawberry.type
class PersonVehiclesConnection:
    page_info: PageInfo
    edges: list[PersonVehiclesEdge | None] | None
    total_count: int | None
    vehicles: list[Vehicle | None] | None


@strawberry.type
class Person(Node):
    name: str | None
    homeworld_id: strawberry.Private[int]
    species_id: strawberry.Private[int | None]
    created: str | None = None
    edited: str | None = None
    gender: str | None = None
    skin_color: str | None = None
    hair_color: str | None = None
    height: int | None = None
    mass: float | None = None
    eye_color: str | None = None
    birth_year: str | None = None

    film_connection: PersonFilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            PersonFilmsConnection,
            FilmsEdge,
            Film,
            attribute_name="films",
            get_additional_filters=lambda root: {
                "characters": {
                    "some": {"id": {"equals": Node.get_id(root)}},
                },
            },
        )
    )

    starship_connection: PersonStarshipsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "starship",
            PersonStarshipsConnection,
            StarshipsEdge,
            Starship,
            attribute_name="starships",
            get_additional_filters=lambda root: {
                "pilots": {
                    "some": {"id": {"equals": Node.get_id(root)}},
                },
            },
        )
    )

    vehicle_connection: PersonVehiclesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "vehicle",
            PersonVehiclesConnection,
            VehiclesEdge,
            Vehicle,
            attribute_name="vehicles",
            get_additional_filters=lambda root: {
                "pilots": {
                    "some": {"id": {"equals": Node.get_id(root)}},
                },
            },
        )
    )

    @strawberry.field
    async def homeworld(self, info: Info[Context, None]) -> Planet | None:
        from .planets import Planet

        db = info.context["db"]

        planet = await db.planet.find_first(where={"id": self.homeworld_id})

        return Planet.from_row(planet) if planet is not None else None

    @strawberry.field
    async def species(self, info: Info[Context, None]) -> Species | None:
        from .species import Species

        db = info.context["db"]

        if self.species_id is None:
            return None

        species = await db.species.find_first(where={"id": self.species_id})

        return Species.from_row(species) if species is not None else None

    @staticmethod
    def from_row(row: prisma.models.Person):
        return Person(
            id=strawberry.ID(Node.get_global_id("people", row.id)),
            name=row.name,
            homeworld_id=row.homeworld_id,
            species_id=row.species_id,
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
    edges: list[PeopleEdge | None] | None
    total_count: int | None
    people: list[Person | None] | None
