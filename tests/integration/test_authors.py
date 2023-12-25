import requests

API_URL = "http://127.0.0.1:8000/api"


def test_get_authors():
    r = requests.get(API_URL + "/authors/")
    r.raise_for_status()
    assert r.status_code == 200


def test_create_author():
    r = requests.post(API_URL + "/authors/", json={"name": "John Doe"})
    r.raise_for_status()
    assert r.status_code == 201
    assert r.json()["name"] == "John Doe"


def test_create_with_error():
    r = requests.post(API_URL + "/authors/", json={})
    assert r.status_code == 400
    assert r.json() == {"name": ["This field is required."]}


def test_update_author():
    r = requests.post(API_URL + "/authors/", json={"name": "John Doe"})
    r.raise_for_status()
    author_data = r.json()
    r = requests.put(API_URL + f"/authors/{author_data['id']}", json={"name": "My name"})
    r.raise_for_status()
    assert r.status_code == 200
    assert r.json()["name"] == "My name"
    assert r.json()["id"] == author_data["id"]


def test_delete_author():
    r = requests.post(API_URL + "/authors/", json={"name": "John Doe"})
    r.raise_for_status()
    author_data = r.json()
    r = requests.delete(API_URL + f"/authors/{author_data['id']}")
    r.raise_for_status()
    assert r.status_code == 204
    r = requests.get(API_URL + f"/authors/{author_data['id']}")
    assert r.status_code == 404
