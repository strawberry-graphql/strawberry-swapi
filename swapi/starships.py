import typing

import strawberry

from tables import people, starships
from utils import get_generic_connection

from .node import Node
from .page_info import PageInfo


def _get_connection(
    root,
    info,
    after: typing.Optional[str] = None,
    first: typing.Optional[int] = None,
    before: typing.Optional[str] = None,
    last: typing.Optional[int] = None,
):
    from .people import PeopleConnection, PeopleEdge

    return get_generic_connection(people, PeopleConnection, PeopleEdge)(
        root, info, after, first, before, last
    )


@strawberry.type
class Starship(Node):
    name: typing.Optional[str]
    created: typing.Optional[str] = None
    edited: typing.Optional[str] = None
    model: typing.Optional[str] = None
    cost_in_credits: typing.Optional[str] = None
    length: typing.Optional[float] = None
    max_atmosphering_speed: typing.Optional[int] = None
    hyperdrive_rating: typing.Optional[float] = None
    crew: typing.Optional[str] = None
    passengers: typing.Optional[str] = None
    cargo_capacity: typing.Optional[float] = None
    manufacturers: typing.Optional[typing.List[str]] = None
    consumables: typing.Optional[str] = None
    MGLT: typing.Optional[int] = None
    starship_class: typing.Optional[str] = None

    pilot_connection: typing.Optional["PeopleConnection"] = strawberry.field(
        resolver=_get_connection
    )

    @staticmethod
    def from_row(row):
        return Starship(
            id=row[starships.c.id],
            name=row[starships.c.name],
            created=row[starships.c.created],
            edited=row[starships.c.edited],
            model=row[starships.c.model],
            cost_in_credits=row[starships.c.cost_in_credits],
            length=row[starships.c.length],
            max_atmosphering_speed=row[starships.c.max_atmosphering_speed],
            crew=row[starships.c.crew],
            passengers=row[starships.c.passengers],
            cargo_capacity=row[starships.c.cargo_capacity],
            hyperdrive_rating=row[starships.c.hyperdrive_rating],
            MGLT=row[starships.c.MGLT],
            starship_class=row[starships.c.starship_class],
        )


@strawberry.type
class StarshipsEdge:
    node: typing.Optional[Starship]
    cursor: str

    @staticmethod
    def from_row(row):
        id_ = row[starships.c.id]

        return StarshipsEdge(cursor=id_, node=Starship.from_row(row))


@strawberry.type
class StarshipsConnection:
    page_info: PageInfo
    edges: typing.List[StarshipsEdge]
    total_count: typing.Optional[int]
    starships: typing.List[typing.Optional[Starship]] = None


@strawberry.type
class PersonStarshipsEdge(StarshipsEdge):
    @staticmethod
    def from_row(row):
        id_ = row[starships.c.id]

        return PersonStarshipsEdge(cursor=id_, node=Starship.from_row(row))


@strawberry.type
class PersonStarshipsConnection(StarshipsConnection):
    edges: typing.List[typing.Optional[PersonStarshipsEdge]]
