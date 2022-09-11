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
class VehiclePilotsEdge:
    cursor: str
    node: Annotated["Person", strawberry.lazy(".people")] | None


@strawberry.type
class VehiclePilotsConnection:
    page_info: PageInfo
    edges: list[VehiclePilotsEdge | None] | None
    total_count: int | None
    pilots: list[Annotated["Person", strawberry.lazy(".people")] | None] | None


@strawberry.type
class VehicleFilmsEdge:
    cursor: str
    node: Annotated["Film", strawberry.lazy(".film")] | None


@strawberry.type
class VehicleFilmsConnection:
    page_info: PageInfo
    edges: list[VehicleFilmsEdge | None] | None
    total_count: int | None
    films: list[Annotated["Film", strawberry.lazy(".film")] | None] | None


@strawberry.type
class Vehicle(Node):
    id: strawberry.ID
    name: str | None
    model: str | None
    vehicle_class: str | None
    manufacturers: list[str | None] | None
    length: float | None
    cost_in_credits: float | None
    crew: str | None
    passengers: str | None
    max_atmosphering_speed: int | None
    cargo_capacity: float | None
    consumables: str | None
    created: str | None = None
    edited: str | None = None

    pilot_connection: VehiclePilotsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "person",
            VehiclePilotsConnection,
            VehiclePilotsEdge,
            "swapi.people.Person",
            attribute_name="pilots",
            get_additional_filters=lambda root: {
                "vehicles": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    film_connection: VehicleFilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            VehicleFilmsConnection,
            VehicleFilmsEdge,
            "swapi.film.Film",
            attribute_name="films",
            get_additional_filters=lambda root: {
                "vehicles": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    @classmethod
    def from_row(cls, row: prisma.models.Vehicle) -> "Vehicle":
        return cls(
            id=strawberry.ID(Node.get_global_id("vehicles", row.id)),
            name=row.name,
            model=row.model,
            vehicle_class=row.vehicle_class,
            manufacturers=json.loads(row.manufacturers),
            length=row.length,
            cost_in_credits=row.cost_in_credits,
            crew=row.crew,
            passengers=row.passengers,
            max_atmosphering_speed=row.max_atmosphering_speed,
            cargo_capacity=row.cargo_capacity,
            consumables=row.consumables,
            created=format_datetime(row.created),
            edited=format_datetime(row.edited),
        )


@strawberry.type
class VehiclesEdge:
    node: Vehicle | None
    cursor: str


@strawberry.type
class VehiclesConnection:
    page_info: PageInfo
    edges: list[VehiclesEdge | None] | None
    total_count: int | None
    vehicles: list[Vehicle | None] | None
