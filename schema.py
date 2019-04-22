import typing

import strawberry
from swapi.film import FilmsConnection, FilmsEdge
from swapi.people import PeopleConnection, PeopleEdge, Person
from swapi.planets import PlanetsConnection, PlanetsEdge
from swapi.starships import StarshipsConnection, StarshipsEdge

from tables import database, movies, people, planets, starships
from utils import get_connection_object


@strawberry.type
class Root:
    @strawberry.field
    async def all_films(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional[FilmsConnection]:
        return await get_connection_object(
            movies,
            FilmsConnection,
            FilmsEdge,
            after=after,
            first=first,
            before=before,
            last=last,
        )

    @strawberry.field
    async def person(
        self,
        info,
        id: typing.Optional[strawberry.ID] = None,
        person_id: typing.Optional[strawberry.ID] = None,
    ) -> typing.Optional[Person]:
        if id is None and person_id is None:
            raise ValueError("must provide id or personID")

        # TODO: relay ids
        id = id or person_id

        query = people.select().where(people.c.id == id)

        row = await database.fetch_one(query=query)

        if not row:
            return None

        return Person.from_row(row)

    @strawberry.field
    async def all_people(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional[PeopleConnection]:
        return await get_connection_object(
            people,
            PeopleConnection,
            PeopleEdge,
            after=after,
            first=first,
            before=before,
            last=last,
        )

    @strawberry.field
    async def all_planets(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional[PlanetsConnection]:
        return await get_connection_object(
            planets,
            PlanetsConnection,
            PlanetsEdge,
            after=after,
            first=first,
            before=before,
            last=last,
        )

    @strawberry.field
    async def all_starships(
        self,
        info,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        before: typing.Optional[str] = None,
        last: typing.Optional[int] = None,
    ) -> typing.Optional[StarshipsConnection]:
        return await get_connection_object(
            starships,
            StarshipsConnection,
            StarshipsEdge,
            after=after,
            first=first,
            before=before,
            last=last,
        )


schema = strawberry.Schema(query=Root)
