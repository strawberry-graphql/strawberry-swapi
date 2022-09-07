import prisma
import strawberry
import json
from strawberry.types.info import Info

from swapi.utils.datetime import format_datetime
from utils import get_connection_object

from .context import Context
from .node import Node
from .page_info import PageInfo
# from .species import FilmSpeciesConnection, SpeciesEdge


@strawberry.type(description="A single film.")
class Film(Node):
    title: str | None = strawberry.field(description="The title of this film.")
    episode_id: int | None = strawberry.field(
        name="episodeID", description="The episode number of this film."
    )
    opening_crawl: str | None = strawberry.field(
        description="The opening paragraphs at the beginning of this film."
    )
    director: str | None = strawberry.field(
        description="The name of the director of this film."
    )
    producers: list[str | None] = strawberry.field(
        description="The name(s) of the producer(s) of this film."
    )
    release_date: str | None = strawberry.field(
        description=(
            "The ISO 8601 date format of film " "release at original creator country."
        )
    )
    created: str | None = strawberry.field(
        description=(
            "The ISO 8601 date format of the time that " "this resource was created."
        )
    )
    edited: str | None = strawberry.field(
        description=(
            "The ISO 8601 date format of the time that " "this resource was edited."
        )
    )

    @classmethod
    def from_row(cls, row: prisma.models.Film) -> "Film":

        return cls(
            # TODO: not sure why the original swapi uses films and not the type name
            id=strawberry.ID(Node.get_global_id("films", row.id)),
            title=row.title,
            episode_id=row.episode_id,
            opening_crawl=row.opening_crawl,
            director=row.director,
            producers=json.loads(row.producers),
            release_date=row.release_date.date().isoformat(),
            created=format_datetime(row.created),
            edited=format_datetime(row.edited),
        )


# TODO: make this generic
@strawberry.type
class FilmsEdge:
    node: Film | None
    cursor: str

    @staticmethod
    def from_row(row: prisma.models.Film) -> "FilmsEdge":

        return FilmsEdge(cursor=str(row.id), node=Film.from_row(row))


@strawberry.type
class FilmsConnection:
    page_info: PageInfo
    edges: list[FilmsEdge | None]
    total_count: int | None
    films: list[Film]
