import json

import prisma
import strawberry

from .node import Node
from .page_info import PageInfo
from .species import Species, SpeciesEdge
from .starships import Starship, StarshipsEdge
from .vehicles import Vehicle, VehiclesEdge
from .planets import Planet, PlanetsEdge
from .utils.connections import get_connection_resolver
from .utils.datetime import format_datetime


@strawberry.type
class FilmSpeciesEdge(SpeciesEdge):
    ...


@strawberry.type
class FilmSpeciesConnection:
    page_info: PageInfo
    edges: list[FilmSpeciesEdge | None]
    total_count: int | None
    species: list[Species]


@strawberry.type
class FilmStarshipsEdge(StarshipsEdge):
    ...


@strawberry.type
class FilmStarshipsConnection:
    page_info: PageInfo
    edges: list[FilmStarshipsEdge | None]
    total_count: int | None
    starships: list[Starship]


@strawberry.type
class FilmVehiclesEdge(VehiclesEdge):
    ...


@strawberry.type
class FilmVehiclesConnection:
    page_info: PageInfo
    edges: list[FilmVehiclesEdge | None]
    total_count: int | None
    vehicles: list[Vehicle]


@strawberry.type
class FilmPlanetsEdge(PlanetsEdge):
    ...


@strawberry.type
class FilmPlanetsConnection:
    page_info: PageInfo
    edges: list[FilmPlanetsEdge | None]
    total_count: int | None
    planets: list[Planet]


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

    species_connection: FilmSpeciesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "species",
            FilmSpeciesConnection,
            FilmSpeciesEdge,
            Species,
            attribute_name="species",
            get_additional_filters=lambda root: {
                "films": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    starship_connection: FilmStarshipsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "starship",
            FilmStarshipsConnection,
            FilmStarshipsEdge,
            Starship,
            attribute_name="starships",
            get_additional_filters=lambda root: {
                "films": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    vehicle_connection: FilmVehiclesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "vehicle",
            FilmVehiclesConnection,
            FilmVehiclesEdge,
            Vehicle,
            attribute_name="vehicles",
            get_additional_filters=lambda root: {
                "films": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    planet_connection: FilmPlanetsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "planet",
            FilmPlanetsConnection,
            FilmPlanetsEdge,
            Planet,
            attribute_name="planets",
            get_additional_filters=lambda root: {
                "films": {"some": {"id": Node.get_id(root)}}
            },
        )
    )

    @classmethod
    def from_row(cls, row: prisma.models.Film) -> "Film":
        return cls(
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
