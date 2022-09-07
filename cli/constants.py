from pathlib import Path

HERE = Path(__file__).parent

REFERENCE_API_URL = "https://swapi-graphql.netlify.app/.netlify/functions/index"
FILMS_QUERY = HERE / "queries/films.graphql"
PEOPLE_QUERY = HERE / "queries/people.graphql"
PLANETS_QUERY = HERE / "queries/planets.graphql"

ALL_QUERIES = [
    FILMS_QUERY,
    PEOPLE_QUERY,
    PLANETS_QUERY,
]
