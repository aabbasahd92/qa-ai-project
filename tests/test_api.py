import pytest
from playwright.sync_api import APIRequestContext, Playwright

@pytest.fixture
def api(playwright: Playwright):
    request = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield request
    request.dispose()

def test_get_all_posts(api: APIRequestContext):
    response = api.get("/posts")
    assert response.status == 200
    body = response.json()
    assert len(body) == 100
    assert body[0]["userId"] == 1

def test_get_single_post(api: APIRequestContext):
    response = api.get("/posts/1")
    assert response.status == 200
    body = response.json()
    assert body["id"] == 1
    assert body["userId"] == 1
    assert "title" in body
    assert "body" in body

def test_create_post(api: APIRequestContext):
    response = api.post("/posts", data={
        "title": "QA Automation Post",
        "body": "Created by Playwright API test",
        "userId": 1
    })
    assert response.status == 201
    body = response.json()
    assert body["title"] == "QA Automation Post"
    assert body["userId"] == 1
    assert "id" in body

def test_update_post(api: APIRequestContext):
    response = api.put("/posts/1", data={
        "id": 1,
        "title": "Updated Title",
        "body": "Updated body",
        "userId": 1
    })
    assert response.status == 200
    body = response.json()
    assert body["title"] == "Updated Title"

def test_delete_post(api: APIRequestContext):
    response = api.delete("/posts/1")
    assert response.status == 200

def test_get_user(api: APIRequestContext):
    response = api.get("/users/1")
    assert response.status == 200
    body = response.json()
    assert body["id"] == 1
    assert "name" in body
    assert "email" in body

def test_post_not_found(api: APIRequestContext):
    response = api.get("/posts/99999")
    assert response.status == 404



def test_create_post_missing_title(api: APIRequestContext):
    response = api.post("/posts", data={
        "body": "No title provided",
        "userId": 1
    })
    assert response.status == 201
    body = response.json()
    assert "title" not in body, "API drops missing fields silently — known behavior"

def test_create_post_invalid_user(api: APIRequestContext):
    response = api.post("/posts", data={
        "title": "Test",
        "body": "Test body",
        "userId": 99999
    })
    assert response.status == 201, "API accepts invalid userId — no validation"
    body = response.json()
    assert body["userId"] == 99999
    assert response.status == 400, f"Expected 400 for invalid userId but got {response.status}"

def test_update_nonexistent_post(api: APIRequestContext):
    response = api.put("/posts/99999", data={
        "title": "Ghost Post",
        "body": "This post does not exist",
        "userId": 1
    })
    assert response.status == 500, "API returns 500 instead of 404 — server crashes on missing resource"
def test_get_comments_for_invalid_post(api: APIRequestContext):
    response = api.get("/posts/99999/comments")
    assert response.status == 200, "API returns 200 with empty list for invalid post"
    body = response.json()
    assert len(body) == 0, "No comments for non-existent post"

def test_post_response_time(api: APIRequestContext):
    import time
    start = time.time()
    response = api.get("/posts")
    duration = time.time() - start
    assert response.status == 200
    assert duration < 3.0, f"Response too slow: {duration:.2f}s — expected under 3s"
