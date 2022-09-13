import json
from typing import TYPE_CHECKING, Annotated

import prisma

import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.connections import get_connection_resolver
from .utils.datetime import format_datetime


if TYPE_CHECKING:
    from .film import Film
    from .people import Person


@strawberry.type
class StarshipPilotsEdge:
    cursor: str
    node: Annotated["Person", strawberry.lazy(".people")] | None


@strawberry.type
class StarshipPilotsConnection:
    page_info: PageInfo
    edges: list[StarshipPilotsEdge | None] | None
    total_count: int | None
    pilots: list[Annotated["Person", strawberry.lazy(".people")] | None] | None


@strawberry.type
class StarshipFilmsEdge:
    cursor: str
    node: Annotated["Film", strawberry.lazy(".film")] | None


@strawberry.type
class StarshipFilmsConnection:
    page_info: PageInfo
    edges: list[StarshipFilmsEdge | None] | None
    total_count: int | None
    films: list[Annotated["Film", strawberry.lazy(".film")] | None] | None


@strawberry.type
class Starship(Node):
    name: str | None
    created: str | None = None
    edited: str | None = None
    model: str | None = None
    cost_in_credits: float | None = None
    length: float | None = None
    max_atmosphering_speed: int | None = None
    hyperdrive_rating: float | None = None
    crew: str | None = None
    passengers: str | None = None
    cargo_capacity: float | None = None
    manufacturers: list[str | None] | None = None
    consumables: str | None = None
    MGLT: int | None = None
    starship_class: str | None = None

    pilot_connection: StarshipPilotsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "person",
            StarshipPilotsConnection,
            StarshipPilotsEdge,
            "swapi.people.Person",
            attribute_name="pilots",
            get_additional_filters=lambda root: {
                "starships": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    film_connection: StarshipFilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            StarshipFilmsConnection,
            StarshipFilmsEdge,
            "swapi.film.Film",
            attribute_name="films",
            get_additional_filters=lambda root: {
                "starships": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    @staticmethod
    def from_row(row: prisma.models.Starship) -> "Starship":
        return Starship(
            id=strawberry.ID(Node.get_global_id("starships", row.id)),
            name=row.name,
            created=format_datetime(row.created),
            edited=format_datetime(row.edited),
            model=row.model,
            cost_in_credits=row.cost_in_credits,
            length=row.length,
            max_atmosphering_speed=row.max_atmosphering_speed,
            hyperdrive_rating=row.hyperdrive_rating,
            crew=row.crew,
            passengers=row.passengers,
            cargo_capacity=row.cargo_capacity,
            manufacturers=json.loads(row.manufacturers),
            consumables=row.consumables,
            MGLT=row.MGLT,
            starship_class=row.starship_class,
        )


@strawberry.type
class StarshipsEdge:
    node: Starship | None
    cursor: str


@strawberry.type
class StarshipsConnection:
    page_info: PageInfo
    edges: list[StarshipsEdge | None] | None
    total_count: int | None
    starships: list[Starship | None] | None
