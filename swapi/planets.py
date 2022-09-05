import typing

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo


@strawberry.type
class Planet(Node):
    name: typing.Optional[str]
    created: typing.Optional[str] = None
    edited: typing.Optional[str] = None
    gravity: typing.Optional[str] = None
    surface_water: typing.Optional[float] = None
    diameter: typing.Optional[int] = None
    rotation_period: typing.Optional[int] = None
    orbital_period: typing.Optional[int] = None
    population: typing.Optional[float] = None

    @staticmethod
    def from_row(row: prisma.models.planet)-> "Planet":
        return Planet(
            id=strawberry.ID(str(row.id)),
            name=row.name,
            # created=row.created,
            # edited=row.edited,
            gravity=row.gravity,
            surface_water=row.surface_water,
            diameter=row.diameter,
            rotation_period=row.rotation_period,
            orbital_period=row.orbital_period,
            population=row.population,
        )


@strawberry.type
class PlanetsEdge:
    node: typing.Optional[Planet]
    cursor: str

    @staticmethod
    def from_row(row):
        id_ = row[planets.c.id]

        return PlanetsEdge(cursor=id_, node=Planet.from_row(row))


@strawberry.type
class PlanetsConnection:
    page_info: PageInfo
    edges: typing.List[PlanetsEdge]
    total_count: int
    planets: typing.List[Planet] = None
