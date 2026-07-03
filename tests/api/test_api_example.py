import pytest
from playwright.sync_api import APIRequestContext, Playwright


@pytest.fixture(scope="module")
def api_context(playwright: Playwright) -> APIRequestContext:
    """Provides a Playwright API request context for HTTP testing."""
    context = playwright.request.new_context()
    yield context
    context.dispose()


@pytest.mark.api
class TestGetRequests:
    def test_fetch_post_from_jsonplaceholder(self, api_context: APIRequestContext):
        response = api_context.get("https://jsonplaceholder.typicode.com/posts/1")

        assert response.status == 200
        assert "application/json" in response.headers["content-type"]

        body = response.json()
        assert body["id"] == 1
        assert "title" in body
        assert "body" in body
        assert "userId" in body

    def test_verify_response_headers_and_status(self, api_context: APIRequestContext):
        response = api_context.get("https://jsonplaceholder.typicode.com/posts")

        assert response.ok
        assert response.status == 200
        assert "application/json" in response.headers["content-type"]

    def test_handle_non_existent_resource(self, api_context: APIRequestContext):
        response = api_context.get("https://jsonplaceholder.typicode.com/posts/99999")

        assert response.status == 404

    def test_query_parameters(self, api_context: APIRequestContext):
        response = api_context.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={"userId": 1, "_limit": 3},
        )

        assert response.status == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) <= 3
        for post in body:
            assert post["userId"] == 1


@pytest.mark.api
class TestPostRequests:
    def test_create_new_resource(self, api_context: APIRequestContext):
        new_post = {
            "title": "Playwright API Testing",
            "body": "This is a test post created via Playwright API",
            "userId": 1,
        }

        response = api_context.post(
            "https://jsonplaceholder.typicode.com/posts",
            data=new_post,
        )

        assert response.status == 201
        body = response.json()
        assert "id" in body
        assert body["title"] == "Playwright API Testing"
        assert "body" in body
        assert body["userId"] == 1


@pytest.mark.api
class TestPutRequests:
    def test_update_existing_resource(self, api_context: APIRequestContext):
        updated_post = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1,
        }

        response = api_context.put(
            "https://jsonplaceholder.typicode.com/posts/1",
            data=updated_post,
        )

        assert response.status == 200
        body = response.json()
        assert body["title"] == "Updated Title"


@pytest.mark.api
class TestDeleteRequests:
    def test_remove_resource(self, api_context: APIRequestContext):
        response = api_context.delete("https://jsonplaceholder.typicode.com/posts/1")

        assert response.status == 200
