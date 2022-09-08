from typing import Callable

import strawberry
from strawberry.types.info import Info

from swapi.context import Context
from swapi.film import Film, FilmsConnection, FilmsEdge
from swapi.people import PeopleConnection, PeopleEdge, Person
from swapi.planets import Planet, PlanetsConnection, PlanetsEdge
from swapi.species import Specie, SpeciesConnection, SpeciesEdge
from swapi.starships import Starship, StarshipsConnection, StarshipsEdge
from swapi.vehicles import Vehicle, VehiclesConnection, VehiclesEdge
from utils import get_connection_object


def _get_connection_resolver(
    table_name: str,
    ConnectionType: type,
    EdgeType: type,
    NodeType: type,
    attribute_name: str,
) -> Callable:
    async def _resolve(
        self,
        info: Info[Context, None],
        after: str | None = None,
        first: int | None = None,
        before: str | None = None,
        last: int | None = None,
    ) -> ConnectionType | None:  # type: ignore
        db = info.context["db"]

        return await get_connection_object(
            getattr(db, table_name),
            ConnectionType,
            EdgeType,
            NodeType,
            after=after,
            first=first,
            before=before,
            last=last,
            attribute_name=attribute_name,
        )

    return _resolve


@strawberry.type
class Root:
    all_films: FilmsConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "film",
            FilmsConnection,
            FilmsEdge,
            Film,
            attribute_name="films",
        )
    )

    all_people: PeopleConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "person",
            PeopleConnection,
            PeopleEdge,
            Person,
            attribute_name="people",
        )
    )

    all_planets: PlanetsConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "planet",
            PlanetsConnection,
            PlanetsEdge,
            Planet,
            attribute_name="planets",
        )
    )

    all_species: SpeciesConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "species",
            SpeciesConnection,
            SpeciesEdge,
            Specie,
            attribute_name="species",
        )
    )

    all_vehicles: VehiclesConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "vehicle",
            VehiclesConnection,
            VehiclesEdge,
            Vehicle,
            attribute_name="vehicles",
        )
    )

    all_starships: StarshipsConnection | None = strawberry.field(
        resolver=_get_connection_resolver(
            "starship",
            StarshipsConnection,
            StarshipsEdge,
            Starship,
            attribute_name="starships",
        )
    )


schema = strawberry.Schema(query=Root)
