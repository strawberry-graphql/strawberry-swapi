import typing

import prisma
import strawberry
from utils import get_connection_object

from .node import Node
from .page_info import PageInfo
from .species import FilmSpeciesConnection, SpeciesEdge


@strawberry.type(description="A single film.")
class Film(Node):
    title: typing.Optional[str] = strawberry.field(
        description="The title of this film."
    )
    episode_id: typing.Optional[int] = strawberry.field(
        name="episodeID", description="The episode number of this film."
    )
    opening_crawl: typing.Optional[str] = strawberry.field(
        description="The opening paragraphs at the beginning of this film."
    )
    director: typing.Optional[str] = strawberry.field(
        description="The name of the director of this film."
    )
    producers: typing.List[typing.Optional[str]] = strawberry.field(
        description="The name(s) of the producer(s) of this film."
    )
    release_date: typing.Optional[str] = strawberry.field(
        description=(
            "The ISO 8601 date format of film "
            "release at original creator country."
        )
    )
    created: typing.Optional[str] = strawberry.field(
        description=(
            "The ISO 8601 date format of the time that "
            "this resource was created."
        )
    )
    edited: typing.Optional[str] = strawberry.field(
        description=(
            "The ISO 8601 date format of the time that "
            "this resource was edited."
        )
    )

    @strawberry.field
    async def species_connection(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional["FilmSpeciesConnection"]:
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
    def from_row(cls, row: prisma.models.film) -> "Film":
        return cls(
            id=strawberry.ID(str(row.id)),
            title=row.title,
            episode_id=row.episode_id,
            opening_crawl=row.opening_crawl,
            director=row.director,
            producers=row.producer.split(","),
            release_date=None,
            created=None,
            edited=None,
        )



@strawberry.type
class FilmsEdge:
    node: typing.Optional[Film]
    cursor: str

    @staticmethod
    def from_row(row: prisma.models.film) -> "FilmsEdge":

        return FilmsEdge(
            cursor=str(row.id   ),
            node=Film.from_row(row)
        )


@strawberry.type
class FilmsConnection:
    page_info: PageInfo
    edges: typing.List[typing.Optional[FilmsEdge]]
    total_count: typing.Optional[int]
