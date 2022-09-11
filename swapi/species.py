import json

import prisma
import strawberry

from strawberry.types.info import Info
from .context import Context

from .node import Node
from .planets import Planet
from .page_info import PageInfo
from .utils.datetime import format_datetime


@strawberry.type
class Species(Node):
    id: strawberry.ID
    name: str
    homeworld_id: strawberry.Private[int | None]
    created: str | None = None
    edited: str | None = None
    classification: str | None = None
    designation: str | None = None
    eye_colors: list[str | None] | None = None
    skin_colors: list[str | None] | None = None
    hair_colors: list[str | None] | None = None
    language: str | None = None
    average_lifespan: int | None = None
    average_height: float | None = None

    @strawberry.field
    async def homeworld(self, info: Info[Context, None]) -> Planet | None:
        from .planets import Planet

        db = info.context["db"]

        if self.homeworld_id is None:
            return None

        planet = await db.planet.find_first(where={"id": self.homeworld_id})

        return Planet.from_row(planet) if planet is not None else None

    @classmethod
    def from_row(cls, row: prisma.models.Species) -> "Species":
        return cls(
            id=strawberry.ID(Node.get_global_id("species", row.id)),
            homeworld_id=row.homeworld_id,
            name=row.name,
            designation=row.designation,
            classification=row.classification,
            eye_colors=json.loads(row.eye_colors),
            skin_colors=json.loads(row.skin_colors),
            hair_colors=json.loads(row.hair_colors),
            language=row.language,
            average_lifespan=row.average_lifespan,
            average_height=row.average_height,
            created=format_datetime(row.created),
            edited=format_datetime(row.edited),
        )


@strawberry.type
class SpeciesEdge:
    node: Species | None
    cursor: str


@strawberry.type
class SpeciesConnection:
    page_info: PageInfo
    edges: list[SpeciesEdge]
    total_count: int
    species: list[Species]
