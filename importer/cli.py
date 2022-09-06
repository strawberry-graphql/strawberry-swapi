import asyncio
import time
from asyncio import run
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import httpx
import prisma
import typer

HERE = Path(__file__).parent


def _parse_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")


def _parse_id(global_id: str) -> int:
    return int(b64decode(global_id).split(b":")[1])


async def wait_host_port(host, port, duration=10, delay=2):
    """Repeatedly try if a port on a host is open until duration seconds passed

    Parameters
    ----------
    host : str
        host ip address or hostname
    port : int
        port number
    duration : int, optional
        Total duration in seconds to wait, by default 10
    delay : int, optional
        delay in seconds between each try, by default 2

    Returns
    -------
    awaitable bool
    """
    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            _reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5
            )
            writer.close()
            await writer.wait_closed()
            return True
        except Exception:
            if delay:
                await asyncio.sleep(delay)
    return False


async def _load_films(db: prisma.Prisma) -> None:
    query = Path(HERE / "queries/films.graphql")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://swapi-graphql.netlify.app/.netlify/functions/index",
            json={"query": query.read_text()},
            headers={"Accept": "application/json"},
        )

        films = response.json()["data"]["allFilms"]["films"]

        # create many is not supported by sqlite

        for film in films:
            await db.film.create(
                data={
                    "id": _parse_id(film["id"]),
                    "title": film["title"],
                    "episode_id": film["episodeID"],
                    "opening_crawl": film["openingCrawl"],
                    "director": film["director"],
                    "producers": ",".join(film["producers"]),
                    "release_date": _parse_date(film["releaseDate"]),
                }
            )


async def _load():
    db = prisma.Prisma()

    await db.connect()

    await db.film.delete_many()

    try:
        await _load_films(db)
    finally:
        await db.disconnect()


app = typer.Typer()


@app.command()
def load_data():
    print("loading data...")
    run(_load())
    print("loaded data")


@app.command()
def test_queries():
    print("Ideally this command would run some queries against the the GraphQL API")


if __name__ == "__main__":
    app()
