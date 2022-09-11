import json
from typing import TYPE_CHECKING, Annotated

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.connections import get_connection_resolver
from .utils.datetime import format_datetime

if TYPE_CHECKING:
    from .people import Person
    from .film import Film


@strawberry.type
class PlanetResidentsEdge:
    cursor: str
    node: Annotated["Person", strawberry.lazy(".people")] | None


@strawberry.type
class PlanetResidentsConnection:
    page_info: PageInfo
    edges: list[PlanetResidentsEdge | None] | None
    total_count: int | None
    residents: list[Annotated["Person", strawberry.lazy(".people")] | None] | None


@strawberry.type
class PlanetFilmsEdge:
    cursor: str
    node: Annotated["Film", strawberry.lazy(".film")] | None


@strawberry.type
class PlanetFilmsConnection:
    page_info: PageInfo
    edges: list[PlanetFilmsEdge | None] | None
    total_count: int | None
    films: list[Annotated["Film", strawberry.lazy(".film")] | None] | None


@strawberry.type
class Planet(Node):
    name: str | None
    created: str | None = None
    edited: str | None = None
    gravity: str | None = None
    surface_water: float | None = None
    diameter: int | None = None
    rotation_period: int | None = None
    orbital_period: int | None = None
    population: float | None = None
    climates: list[str | None] | None = None
    terrains: list[str | None] | None = None

    resident_connection: PlanetResidentsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "person",
            PlanetResidentsConnection,
            PlanetResidentsEdge,
            "swapi.people.Person",
            attribute_name="residents",
            get_additional_filters=lambda root: {
                "homeworld": {"id": Node.get_id(root)}
            },
        )
    )

    film_connection: PlanetFilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            PlanetFilmsConnection,
            PlanetFilmsEdge,
            "swapi.film.Film",
            attribute_name="films",
            get_additional_filters=lambda root: {
                "planets": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    @staticmethod
    def from_row(row: prisma.models.Planet) -> "Planet":
        return Planet(
            id=strawberry.ID(Node.get_global_id("planets", row.id)),
            name=row.name,
            gravity=row.gravity,
            surface_water=row.surface_water,
            diameter=row.diameter,
            rotation_period=row.rotation_period,
            orbital_period=row.orbital_period,
            population=row.population,
            climates=json.loads(row.climates),
            terrains=json.loads(row.terrains),
            edited=format_datetime(row.edited),
            created=format_datetime(row.created),
        )


@strawberry.type
class PlanetsEdge:
    node: Planet | None
    cursor: str


@strawberry.type
class PlanetsConnection:
    page_info: PageInfo
    edges: list[PlanetsEdge | None] | None
    total_count: int | None
    planets: list[Planet | None] | None
