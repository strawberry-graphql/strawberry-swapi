from swapi.page_info import PageInfo

from tables import database


async def get_connection_object(
    table,
    ConnectionType,
    EdgeType,
    *,
    after=None,
    before=None,
    first=None,
    last=None
):
    """Returns a ConnectionType instance based on EdgeType and the passed params.

    This is based on the Relay Connection specification, see it here:
    https://facebook.github.io/relay/graphql/connections.htm
    """

    count = await database.fetch_val(query=table.count())

    query = table.select().order_by(table.c.id)

    # TODO: not sure this is 100% correct
    # TODO: fetch if has next/prev pages

    limit = first or last or 10
    offset = count - last if last else 0

    query = query.limit(limit).offset(offset)

    if after:
        query = query.where(table.c.id > after)

    if before:
        query = query.where(table.c.id < before)

    rows = await database.fetch_all(query=query)

    return ConnectionType(
        page_info=PageInfo(has_next_page=False, has_previous_page=False),
        edges=[EdgeType.from_row(row) for row in rows],
        total_count=count,
    )
