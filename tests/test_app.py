from importlib.resources import contents, read_text

import pytest
from starlette.testclient import TestClient

from app import app

QUERIES = [name for name in contents("data") if name.endswith(".graphql")]


@pytest.fixture
def client():
    return TestClient(app)


def test_graphql_page(client):
    response = client.get("/graphql")

    assert response.status_code == 200


@pytest.mark.parametrize("name", QUERIES)
def test_responses(client, name):
    text = read_text("data", name)
    response = client.post("/graphql", json={"query": text})
    data = response.json()

    assert not data["errors"]
    assert data["data"]
