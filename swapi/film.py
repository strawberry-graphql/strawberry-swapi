import prisma
import strawberry
from strawberry.types.info import Info
from utils import get_connection_object

from .context import Context
from .node import Node
from .page_info import PageInfo
from .species import FilmSpeciesConnection, SpeciesEdge


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

    @strawberry.field
    async def species_connection(
        self,
        info: Info[Context, None],
        after: str | None = None,
        first: int | None = None,
        before: str | None = None,
        last: int | None = None,
    ) -> FilmSpeciesConnection | None:
        # TODO: filtering

        return await get_connection_object(
            species,
            FilmSpeciesConnection,
            SpeciesEdge,
            after=after,
            first=first,
            before=before,
            last=last,
        )

    @classmethod
    def from_row(cls, row: prisma.models.Film) -> "Film":
        # format created as 2014-12-10T14:23:31.880000Z
        # format edited as 2014-12-20T19:49:45.256000Z
        created = row.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        edited = row.edited.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        return cls(
            # TODO: not sure why the original swapi uses films and not the type name
            id=strawberry.ID(Node.get_global_id("films", row.id)),
            title=row.title,
            episode_id=row.episode_id,
            opening_crawl=row.opening_crawl,
            director=row.director,
            producers=row.producers.split(","),
            release_date=row.release_date.date().isoformat(),
            created=created,
            edited=edited,
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
