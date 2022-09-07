import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.datetime import format_datetime


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
            climates=row.climates.split(","),
            terrains=row.terrains.split(","),
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
    edges: list[PlanetsEdge]
    total_count: int
    planets: list[Planet]
