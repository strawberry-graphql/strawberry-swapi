import asyncio

import prisma
import typer
from jsondiff import diff

from .constants import ALL_QUERIES, REFERENCE_API_URL
from .importer import Importer
from .utils.query import query
from .utils.wait_for_port import wait_for_port

app = typer.Typer()


@app.command()
def import_data():
    async def _import():
        db = prisma.Prisma()

        await db.connect()

        importer = Importer(db)

        try:
            await importer.import_all()
        finally:
            await db.disconnect()

    print("importing data...")
    asyncio.run(_import())
    print("loaded data")


@app.command()
def test_queries():
    print("Ideally this command would run some queries against the the GraphQL API")

    async def _test():
        if not await wait_for_port("localhost", 8000):
            print("The server is not running")
            return

        for query_path in ALL_QUERIES:
            text = query_path.read_text()

            reference, implementation = await asyncio.gather(
                query(REFERENCE_API_URL, text),
                query("http://localhost:8000/graphql", text),
            )

            difference = diff(reference, implementation, syntax="symmetric")

            if difference:
                print(f"Query {query_path} is different")
                print(difference)

    print("running queries...")
    asyncio.run(_test())
    print("ran queries")
