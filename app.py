import uvicorn
from starlette.applications import Starlette
from strawberry.contrib.starlette import GraphQLApp

from schema import schema
from tables import database

app = Starlette()
app.debug = False

app.add_route("/graphql", GraphQLApp(schema))


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
