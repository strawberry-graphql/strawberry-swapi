from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from prisma import Prisma
from schema import schema

from strawberry.fastapi import GraphQLRouter


db = Prisma()
app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


async def get_context():
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return RedirectResponse(url="/graphql")
