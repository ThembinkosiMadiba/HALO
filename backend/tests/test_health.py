from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def make_client(**overrides) -> TestClient:
    settings = Settings(_env_file=None, **overrides)
    return TestClient(create_app(settings), raise_server_exceptions=False)


def test_health_returns_ok():
    response = make_client().get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_responses_carry_security_headers():
    response = make_client().get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_api_docs_are_hidden_in_production():
    client = make_client()
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(path).status_code == 404


def test_api_docs_are_available_in_development():
    client = make_client(environment="development")
    assert client.get("/openapi.json").status_code == 200


def test_unknown_path_returns_plain_404():
    response = make_client().get("/does-not-exist")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_unhandled_error_response_is_generic():
    app = create_app(Settings(_env_file=None))

    @app.get("/boom")
    def boom():
        raise RuntimeError("internal secret detail")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert "internal secret detail" not in response.text
