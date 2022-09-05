import typing

import strawberry

from tables import people, starships
from utils import get_connection_object

from .page_info import PageInfo
from .node import Node


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

    @strawberry.field
    async def pilot_connection(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional[strawberry.LazyType["PeopleConnection", ".people"]]:
        from .people import PeopleConnection, PeopleEdge

        # TODO: filtering

        return await get_connection_object(
            people,
            PeopleConnection,
            PeopleEdge,
            after=after,
            first=first,
            before=before,
            last=last,
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
