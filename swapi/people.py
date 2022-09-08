import prisma
import strawberry
from strawberry.types.info import Info

from swapi.utils.datetime import format_datetime

from .context import Context
from .film import Film, FilmsConnection, FilmsEdge
from .node import Node
from .page_info import PageInfo
from .planets import Planet
from .species import Species
from .starships import Starship, StarshipsConnection, StarshipsEdge
from .utils.connections import get_connection_resolver
from .vehicles import Vehicle, VehiclesConnection, VehiclesEdge


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

    film_connection: FilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            FilmsConnection,
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

    starship_connection: StarshipsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "starship",
            StarshipsConnection,
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

    vehicle_connection: VehiclesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "vehicle",
            VehiclesConnection,
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
    edges: list[PeopleEdge]
    total_count: int
    people: list[Person]
