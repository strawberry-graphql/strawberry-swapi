import json

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .utils.datetime import format_datetime


@strawberry.type
class Specie(Node):
    id: strawberry.ID
    name: str
    created: str | None = None
    edited: str | None = None
    classification: str | None = None
    designation: str | None = None
    eye_colors: list[str | None] | None = None
    skin_colors: list[str | None] | None = None
    hair_colors: list[str | None] | None = None
    language: str | None = None
    average_lifespan: int | None = None
    average_height: int | None = None

    @classmethod
    def from_row(cls, row: prisma.models.Species) -> "Specie":
        return cls(
            id=strawberry.ID(Node.get_global_id("species", row.id)),
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
    node: Specie | None
    cursor: str


@strawberry.type
class SpeciesConnection:
    page_info: PageInfo
    edges: list[SpeciesEdge]
    total_count: int
    species: list[Specie]
