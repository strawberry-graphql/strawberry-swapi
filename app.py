import uvicorn
from starlette.applications import Starlette
from strawberry.asgi import GraphQL

from schema import schema
from tables import database

app = Starlette()
app.debug = False

app.add_route("/graphql", GraphQL(schema))


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
