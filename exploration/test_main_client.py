import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

import main


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    main.app.dependency_overrides[main.get_session] = get_test_session

    with TestClient(main.app) as test_client:
        yield test_client

    main.app.dependency_overrides.clear()


def create_note(client, **overrides):
    payload = {
        "title": "Test Note",
        "content": "Test content",
        "category": "work",
        "tags": ["test", "pytest"],
    }
    payload.update(overrides)

    response = client.post("/notes", json=payload)

    assert response.status_code == 201, response.text
    return response.json()


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_simple_path_endpoints(client):
    name_response = client.get("/name/Maxi")
    sum_response = client.get("/summe/2/3")

    assert name_response.status_code == 200
    assert name_response.json() == {"message": "Hello, Maxi!"}
    assert sum_response.status_code == 200
    assert sum_response.json() == {"message": "Die Summe aus 2 + 3 = 5"}


def test_create_note_returns_note_with_id_and_tags(client):
    note = create_note(
        client,
        title="Team Meeting",
        content="Discuss project",
        category="work",
        tags=["urgent", "meeting"],
    )

    assert isinstance(note["id"], int)
    assert note["title"] == "Team Meeting"
    assert note["content"] == "Discuss project"
    assert note["category"] == "work"
    assert sorted(note["tags"]) == ["meeting", "urgent"]
    assert "created_at" in note


def test_tags_are_cleaned_lowercase_and_deduplicated(client):
    note = create_note(client, tags=["  URGENT  ", "urgent", "Meeting"])

    assert sorted(note["tags"]) == ["meeting", "urgent"]


def test_list_notes_with_combined_filters(client):
    matching_note = create_note(
        client,
        title="Team Meeting",
        content="Discuss release",
        category="work",
        tags=["urgent"],
    )
    create_note(
        client,
        title="Private Meeting",
        content="Discuss weekend",
        category="personal",
        tags=["urgent"],
    )

    response = client.get(
        "/notes",
        params={"category": "work", "tag": "urgent", "search": "meeting"},
    )
    notes = response.json()

    assert response.status_code == 200
    assert [note["id"] for note in notes] == [matching_note["id"]]


def test_get_patch_put_and_delete_note(client):
    note = create_note(client, title="Original", content="old")
    note_id = note["id"]

    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Original"

    patch_response = client.patch(
        f"/notes/{note_id}",
        json={"title": "Patched"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "Patched"
    assert patch_response.json()["content"] == "old"

    put_response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "Replaced",
            "content": "new",
            "category": "personal",
            "tags": ["done"],
        },
    )
    assert put_response.status_code == 200
    assert put_response.json()["title"] == "Replaced"
    assert put_response.json()["category"] == "personal"
    assert put_response.json()["tags"] == ["done"]

    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/notes/{note_id}")
    assert missing_response.status_code == 404


def test_stats_categories_and_tags(client):
    create_note(client, category="work", tags=["urgent", "meeting"])
    create_note(client, category="personal", tags=["urgent"])

    stats_response = client.get("/notes/stats")
    categories_response = client.get("/categories")
    tags_response = client.get("/tags")
    urgent_notes_response = client.get("/tags/urgent/notes")

    assert stats_response.status_code == 200
    assert stats_response.json()["total_notes"] == 2
    assert stats_response.json()["by_category"] == {"work": 1, "personal": 1}
    assert categories_response.json() == ["personal", "work"]
    assert tags_response.json() == ["meeting", "urgent"]
    assert len(urgent_notes_response.json()) == 2


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "Only title"},
        {"title": "x", "content": "x", "category": "x", "tags": "not-a-list"},
        {"title": "x", "content": "x", "category": "x", "tags": ["a"]},
        {
            "title": "x",
            "content": "x",
            "category": "x",
            "tags": [f"tag{i}" for i in range(11)],
        },
    ],
)
def test_create_note_validation_errors(client, payload):
    response = client.post("/notes", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "params",
    [
        {"created_after": "not-a-date"},
        {"created_before": "2026-99-99"},
    ],
)
def test_invalid_date_filters_return_422(client, params):
    response = client.get("/notes", params=params)

    assert response.status_code == 422


def test_missing_note_returns_404(client):
    response = client.get("/notes/999999")

    assert response.status_code == 404


def test_query_parameters_filters_names(client):
    response = client.get("/queryparameters", params={"param1": "li", "param2": 7})

    assert response.status_code == 200
    assert response.json() == {
        "param1": "li",
        "param2": 7,
        "namen": ["Alice", "Charlie"],
    }
