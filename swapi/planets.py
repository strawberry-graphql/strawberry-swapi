import typing

import strawberry

from tables import planets

from .page_info import PageInfo
from .node import Node


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
    def from_row(row):
        return Planet(
            id=row[planets.c.id],
            name=row[planets.c.name],
            created=row[planets.c.created],
            edited=row[planets.c.edited],
            gravity=row[planets.c.gravity],
            surface_water=row[planets.c.surface_water],
            diameter=row[planets.c.diameter],
            rotation_period=row[planets.c.rotation_period],
            orbital_period=row[planets.c.orbital_period],
            population=row[planets.c.population],
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
