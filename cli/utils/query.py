import httpx


async def query(
    url: str, query: str, variables: dict[str, dict] | None = None
) -> dict[str, dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"query": query, "variables": variables},
            headers={"Accept": "application/json"},
        )

    response.raise_for_status()
    return response.json()
