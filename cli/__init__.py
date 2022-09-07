import asyncio
import time
from asyncio import run
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import httpx
import prisma
import typer

from .utils.wait_for_port import wait_for_port

HERE = Path(__file__).parent


def _parse_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")


def _parse_id(global_id: str) -> int:
    return int(b64decode(global_id).split(b":")[1])


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


app = typer.Typer()


@app.command()
def load_data():
    async def _load():
        db = prisma.Prisma()

        await db.connect()

        await db.film.delete_many()

        try:
            await _load_films(db)
        finally:
            await db.disconnect()

    print("loading data...")
    run(_load())
    print("loaded data")


@app.command()
def test_queries():
    print("Ideally this command would run some queries against the the GraphQL API")

    async def _test():
        if not await wait_for_port("localhost", 8000):
            print("The server is not running")
            return

    print("running queries...")
    run(_test())
    print("ran queries")
