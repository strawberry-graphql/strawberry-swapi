from typing import Annotated

import strawberry
from strawberry.types.info import Info

from swapi.context import Context
from swapi.film import Film, FilmsConnection, FilmsEdge
from swapi.node import Node
from swapi.people import PeopleConnection, PeopleEdge, Person
from swapi.planets import Planet, PlanetsConnection, PlanetsEdge
from swapi.species import Species, SpeciesConnection, SpeciesEdge
from swapi.starships import Starship, StarshipsConnection, StarshipsEdge
from swapi.utils.connections import get_connection_resolver
from swapi.vehicles import Vehicle, VehiclesConnection, VehiclesEdge


@strawberry.type
class Root:
    all_films: FilmsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "film",
            FilmsConnection,
            FilmsEdge,
            Film,
            attribute_name="films",
        )
    )

    all_people: PeopleConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "person",
            PeopleConnection,
            PeopleEdge,
            Person,
            attribute_name="people",
        )
    )

    all_planets: PlanetsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "planet",
            PlanetsConnection,
            PlanetsEdge,
            Planet,
            attribute_name="planets",
        )
    )

    all_species: SpeciesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "species",
            SpeciesConnection,
            SpeciesEdge,
            Species,
            attribute_name="species",
        )
    )

    all_vehicles: VehiclesConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "vehicle",
            VehiclesConnection,
            VehiclesEdge,
            Vehicle,
            attribute_name="vehicles",
        )
    )

    all_starships: StarshipsConnection | None = strawberry.field(
        resolver=get_connection_resolver(
            "starship",
            StarshipsConnection,
            StarshipsEdge,
            Starship,
            attribute_name="starships",
        )
    )

    @strawberry.field
    def film(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        film_id: Annotated[strawberry.ID | None, strawberry.argument(name="filmID")],
    ) -> Film | None:
        return None

    @strawberry.field
    def person(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        person_id: Annotated[
            strawberry.ID | None, strawberry.argument(name="personID")
        ],
    ) -> Person | None:
        return None

    @strawberry.field
    def planet(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        planet_id: Annotated[
            strawberry.ID | None, strawberry.argument(name="planetID")
        ],
    ) -> Planet | None:
        return None

    @strawberry.field
    def species(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        species_id: Annotated[
            strawberry.ID | None, strawberry.argument(name="speciesID")
        ],
    ) -> Species | None:
        return None

    @strawberry.field
    def vehicle(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        vehicle_id: Annotated[
            strawberry.ID | None, strawberry.argument(name="vehicleID")
        ],
    ) -> Vehicle | None:
        return None

    @strawberry.field
    def starship(
        self,
        info: Info[Context, None],
        id: strawberry.ID | None,
        starship_id: Annotated[
            strawberry.ID | None, strawberry.argument(name="starshipID")
        ],
    ) -> Starship | None:
        return None

    @strawberry.field
    def node(
        self,
        info: Info[Context, None],
        id: strawberry.ID,
    ) -> Node | None:
        # TODO: implement this
        return None


schema = strawberry.Schema(query=Root)
