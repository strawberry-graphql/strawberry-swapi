import json

import prisma
import strawberry

from typing import TYPE_CHECKING, Annotated

from .node import Node
from .page_info import PageInfo
from .utils.datetime import format_datetime
from .utils.connections import get_connection_resolver

if TYPE_CHECKING:
    from .people import Person


@strawberry.type
class StarshipPilotsEdge:
    cursor: str
    node: Annotated["Person", strawberry.lazy(".people")]


@strawberry.type
class StarshipPilotsConnection:
    page_info: PageInfo
    edges: list[StarshipPilotsEdge | None]
    total_count: int | None
    pilots: list[Annotated["Person", strawberry.lazy(".people")]]


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
    manufacturers: list[str] | None = None
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
    edges: list[StarshipsEdge]
    total_count: int | None
    starships: list[Starship | None]
