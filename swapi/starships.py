import json
import typing

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.datetime import format_datetime


@strawberry.type
class Starship(Node):
    name: str | None
    created: str | None = None
    edited: str | None = None
    model: str | None = None
    cost_in_credits: float | None = None
    length: float | None = None
    max_atmosphering_speed: typing.Optional[int] = None
    hyperdrive_rating: float | None = None
    crew: str | None = None
    passengers: str | None = None
    cargo_capacity: float | None = None
    manufacturers: list[str] | None = None
    consumables: str | None = None
    MGLT: typing.Optional[int] = None
    starship_class: str | None = None

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
    node: typing.Optional[Starship]
    cursor: str


@strawberry.type
class StarshipsConnection:
    page_info: PageInfo
    edges: typing.List[StarshipsEdge]
    total_count: typing.Optional[int]
    starships: list[Starship | None]
