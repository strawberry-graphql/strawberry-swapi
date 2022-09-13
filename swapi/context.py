from typing import TypedDict

from prisma import Prisma
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response


class Context(TypedDict):
    request: Request
    db: Prisma
    background_tasks: BackgroundTasks
    response: Response
