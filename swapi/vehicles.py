import json

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.datetime import format_datetime


@strawberry.type
class Vehicle(Node):
    id: strawberry.ID
    name: str
    model: str
    vehicle_class: str
    manufacturers: list[str]
    length: float | None
    cost_in_credits: float | None
    crew: str
    passengers: str
    max_atmosphering_speed: int | None
    cargo_capacity: float | None
    consumables: str
    created: str | None = None
    edited: str | None = None

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
    edges: list[VehiclesEdge]
    total_count: int
    vehicles: list[Vehicle]
