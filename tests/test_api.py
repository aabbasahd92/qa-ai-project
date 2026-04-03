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
