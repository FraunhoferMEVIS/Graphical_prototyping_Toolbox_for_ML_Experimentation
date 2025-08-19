import os
import shutil
import pytest
from tests.conftest import projects_dir

from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def with_empty_dir():
    # 1. before test: provide empty directory
    if os.path.exists(projects_dir):
        shutil.rmtree(projects_dir)
    os.makedirs(projects_dir, exist_ok=True)

    # 2. yield to run tests
    yield

    # 3. after test: delete directory
    shutil.rmtree(projects_dir)


@pytest.fixture(scope="function")
def client(with_empty_dir):
    from service.main import app

    yield TestClient(app)


def test_should_get_empty_list(client):
    # when
    response = client.get("/projects")

    # then
    assert response.status_code == 200
    assert response.json() == []


def test_should_get_projects(client):
    # given
    client.post("/projects", json={"id": "A"})
    client.post("/projects", json={"id": "B"})
    client.post("/projects", json={"id": "C"})

    # when
    response = client.get("/projects")

    # then
    assert response.status_code == 200
    assert set(response.json()) == set(("A", "B", "C"))


def test_should_create_project(client):
    # given
    project = "my-new-project"

    # when
    response = client.post("/projects", json={"id": project})

    # then
    assert response.status_code == 200
    response_get = client.get("/projects")
    assert response_get.json() == [project]


def test_should_fail_creating_existing_project(client):
    # given
    project = "my-project"
    client.post("/projects", json={"id": project})

    # when
    response = client.post("/projects", json={"id": project})

    # then
    assert response.status_code == 400


def test_should_rename_project(client):
    # given
    project = "my-project"
    client.post("/projects", json={"id": project})

    # when
    response = client.put(f"/projects/{project}", json={"id": "renamed project"})

    # then
    assert response.status_code == 200
    client.get("/projects").json() == ["renamed project"]


def test_should_fail_rename_collision(client):
    # given
    project = "my-project"
    existing_project = "Existing project"
    client.post("/projects", json={"id": project})
    client.post("/projects", json={"id": existing_project})

    # when
    response = client.put(f"/projects/{project}", json={"id": existing_project})

    # then
    assert response.status_code == 400
    set(client.get("/projects").json()) == set([project, existing_project])


def test_should_delete_project(client):
    # given
    project = "my-new-project"
    other_project = "my-other-project"
    client.post("/projects", json={"id": project})
    client.post("/projects", json={"id": other_project})

    # when
    response = client.delete(f"/projects/{project}")

    # then
    assert response.status_code == 200
    response_get = client.get("/projects")
    assert response_get.json() == [other_project]


def test_should_fail_delete_unknown_project(client):
    # given
    project = "my-project"
    client.post("/projects", json={"id": project})

    # when
    response = client.delete(f"/projects/my-unknown-project")

    # then
    assert response.status_code == 404
