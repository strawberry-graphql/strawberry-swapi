# from typing import Annotated, Optional

# import strawberry
# from strawberry.types.info import Info

# from swapi.context import Context
# from swapi.film import FilmsConnection, FilmsEdge
# from swapi.people import PeopleConnection, PeopleEdge, Person
# from swapi.planets import PlanetsConnection, PlanetsEdge
# from swapi.starships import StarshipsConnection, StarshipsEdge
# from utils import get_connection_object


# @strawberry.type
# class Root:
#     @strawberry.field
#     async def all_films(
#         self,
#         info: Info[Context, None],
#         after: str | None = None,
#         first: int | None = None,
#         before: str | None = None,
#         last: int | None = None,
#     ) -> FilmsConnection | None:
#         db = info.context["db"]

#         return await get_connection_object(
#             db.film,
#             FilmsConnection,
#             FilmsEdge,
#             after=after,
#             first=first,
#             before=before,
#             last=last,
#         )

#     @strawberry.field
#     async def person(
#         self,
#         info: Info[Context, None],
#         id: strawberry.ID | None = None,
#         person_id: Annotated[
#             strawberry.ID | None, strawberry.argument(name="personID")
#         ] = None,
#     ) -> Person | None:
#         if id is None and person_id is None:
#             raise ValueError("must provide id or personID")

#         # TODO: relay ids
#         id = id or person_id

#         db = info.context["db"]

#         person = await db.people.find_first(
#             where={"id": int(id or person_id)}  # type: ignore - we know it's not None
#         )

#         return Person.from_row(person) if person is not None else None

#     @strawberry.field
#     async def all_people(
#         self,
#         info: Info[Context, None],
#         after: str | None = None,
#         first: int | None = None,
#         before: str | None = None,
#         last: int | None = None,
#     ) -> PeopleConnection | None:
#         db = info.context["db"]

#         return await get_connection_object(
#             db.people,
#             PeopleConnection,
#             PeopleEdge,
#             after=after,
#             first=first,
#             before=before,
#             last=last,
#         )

#     @strawberry.field
#     async def all_planets(
#         self,
#         info: Info[Context, None],
#         after: str | None = None,
#         first: int | None = None,
#         before: str | None = None,
#         last: int | None = None,
#     ) -> PlanetsConnection | None:
#         db = info.context["db"]

#         return await get_connection_object(
#             db.planet,
#             PlanetsConnection,
#             PlanetsEdge,
#             after=after,
#             first=first,
#             before=before,
#             last=last,
#         )

#     @strawberry.field
#     async def all_starships(
#         self,
#         info: Info[Context, None],
#         after: str | None = None,
#         first: int | None = None,
#         before: str | None = None,
#         last: int | None = None,
#     ) -> StarshipsConnection | None:
#         db = info.context["db"]

#         return await get_connection_object(
#             db.starship,
#             StarshipsConnection,
#             StarshipsEdge,
#             after=after,
#             first=first,
#             before=before,
#             last=last,
#         )


import strawberry

@strawberry.type
class Root:
    h: str

schema = strawberry.Schema(query=Root)
