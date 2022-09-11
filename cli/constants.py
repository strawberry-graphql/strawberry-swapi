from pathlib import Path

HERE = Path(__file__).parent

REFERENCE_API_URL = "https://swapi-graphql.netlify.app/.netlify/functions/index"
FILMS_QUERY = HERE / "queries/films.graphql"
PEOPLE_QUERY = HERE / "queries/people.graphql"
PLANETS_QUERY = HERE / "queries/planets.graphql"
SPECIES_QUERY = HERE / "queries/species.graphql"
VEHICLES_QUERY = HERE / "queries/vehicles.graphql"
STARSHIP_QUERY = HERE / "queries/starships.graphql"
INTROSPECTION_QUERY = HERE / "queries/introspection.graphql"
PAGINATION_QUERY = HERE / "queries/pagination.graphql"

ALL_QUERIES = [
    FILMS_QUERY,
    PEOPLE_QUERY,
    PLANETS_QUERY,
    SPECIES_QUERY,
    VEHICLES_QUERY,
    STARSHIP_QUERY,
    PAGINATION_QUERY,
]
