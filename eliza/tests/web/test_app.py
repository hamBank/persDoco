import pytest

from eliza_chat.persona import PERSONA_NAME
from eliza_chat.web.app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY="test-secret")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_page_shows_the_persona_name(client):
    response = client.get("/")
    assert response.status_code == 200
    assert PERSONA_NAME.encode() in response.data


def test_start_returns_the_scripts_initial_greeting(client):
    response = client.post("/api/start")
    assert response.status_code == 200
    data = response.get_json()
    assert data["reply"] == "How do you do.  Please tell me your problem."
    assert data["ended"] is False


def test_chat_returns_a_reply_after_start(client):
    client.post("/api/start")
    response = client.post("/api/chat", json={"message": "My mother never listens to me"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["reply"] == "Tell me more about your family."
    assert data["ended"] is False


def test_chat_without_start_creates_a_fresh_conversation_implicitly(client):
    response = client.post("/api/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.get_json()["reply"]


def test_chat_requires_a_message(client):
    client.post("/api/start")
    response = client.post("/api/chat", json={})
    assert response.status_code == 400


def test_conversation_memory_is_carried_across_requests(client, monkeypatch):
    monkeypatch.setattr("eliza_chat.classic.engine.random.randrange", lambda n: 0)
    client.post("/api/start")
    client.post("/api/chat", json={"message": "My job is boring"})
    response = client.post("/api/chat", json={"message": "xyzzy plugh"})
    data = response.get_json()
    assert data["reply"] == "Lets discuss further why your job is boring ."


def test_chat_ends_the_conversation_on_a_quit_word(client):
    client.post("/api/start")
    response = client.post("/api/chat", json={"message": "bye"})
    data = response.get_json()
    assert data["ended"] is True
    assert data["reply"] == "Goodbye.  Thank you for talking to me."


def test_two_clients_have_independent_conversations(app, monkeypatch):
    monkeypatch.setattr("eliza_chat.classic.engine.random.randrange", lambda n: 0)
    client_a = app.test_client()
    client_b = app.test_client()

    client_a.post("/api/start")
    client_a.post("/api/chat", json={"message": "My job is boring"})

    client_b.post("/api/start")
    response_b = client_b.post("/api/chat", json={"message": "xyzzy plugh"})

    assert response_b.get_json()["reply"] != "Lets discuss further why your job is boring ."
