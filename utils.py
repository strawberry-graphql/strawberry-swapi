from typing import Callable

from strawberry.types.info import Info

from swapi.context import Context
from swapi.page_info import PageInfo


async def get_connection_object(
    table, ConnectionType, EdgeType, *, after=None, before=None, first=None, last=None
):
    """Returns a ConnectionType instance based on EdgeType and the passed params.

    This is based on the Relay Connection specification, see it here:
    https://facebook.github.io/relay/graphql/connections.htm
    """

    if first is None and last is None:
        first = 10

    take = first
    cursor = after

    if take is None:
        assert last is not None

        take = -last
        cursor = before

    count = await table.count()
    data = await table.find_many(
        cursor={"id": int(cursor)} if cursor else None,
        take=take,
        # skip the cursor
        skip=1 if cursor else 0,
        # order={"id": "asc"},
    )

    # TODO: fetch if has next/prev pages

    return ConnectionType(
        page_info=PageInfo(has_next_page=False, has_previous_page=False),
        edges=[EdgeType.from_row(row) for row in data],
        total_count=count,
    )


def get_generic_connection(
    table_name: str, ConnectionType: type, EdgeType: type
) -> Callable:
    async def _connection(
        root: object,
        info: Info[Context, None],
        after: str | None = None,
        first: int | None = None,
        before: str | None = None,
        last: int | None = None,
    ):
        db = info.context["db"]

        # TODO: filter
        table = getattr(db, table_name)

        return await get_connection_object(
            table,
            ConnectionType,
            EdgeType,
            after=after,
            first=first,
            before=before,
            last=last,
        )

    return _connection
