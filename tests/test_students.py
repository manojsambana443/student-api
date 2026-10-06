import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app

def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Student API is running"
    }


def test_create_student_missing_fields():
    client = app.test_client()

    response = client.post(
        "/api/v1/students",
        json={}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "name and course are required"
    }


def test_create_student_missing_course():
    client = app.test_client()

    response = client.post(
        "/api/v1/students",
        json={"name": "Manoj"}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "name and course are required"
    }

def test_create_student():
    client = app.test_client()

    response = client.post(
        "/api/v1/students",
        json={
            "name": "Pytest Student",
            "course": "Testing"
        }
    )

    assert response.status_code == 201

    student = response.get_json()
    assert student["name"] == "Pytest Student"
    assert student["course"] == "Testing"
    assert "id" in student

    cleanup_response = client.delete(
        f"/api/v1/students/{student['id']}"
    )

    assert cleanup_response.status_code == 200


def test_get_student_by_id():
    client = app.test_client()

    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "GET Test Student",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201
    student_id = create_response.get_json()["id"]

    response = client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "GET Test Student"
    assert response.get_json()["course"] == "Python"

    cleanup_response = client.delete(
        f"/api/v1/students/{student_id}"
    )
    assert cleanup_response.status_code == 200


def test_update_student():
    client = app.test_client()

    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "Update Test Student",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201
    student_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/v1/students/{student_id}",
        json={
            "name": "Updated Student",
            "course": "DevOps"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated Student"
    assert response.get_json()["course"] == "DevOps"

    cleanup_response = client.delete(
        f"/api/v1/students/{student_id}"
    )
    assert cleanup_response.status_code == 200


def test_patch_student():
    client = app.test_client()

    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "PATCH Test Student",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201
    student_id = create_response.get_json()["id"]

    response = client.patch(
        f"/api/v1/students/{student_id}",
        json={"course": "Azure DevOps"}
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "PATCH Test Student"
    assert response.get_json()["course"] == "Azure DevOps"

    cleanup_response = client.delete(
        f"/api/v1/students/{student_id}"
    )
    assert cleanup_response.status_code == 200



def test_delete_student():
    client = app.test_client()

    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "DELETE Test Student",
            "course": "Testing"
        }
    )

    assert create_response.status_code == 201
    student_id = create_response.get_json()["id"]

    delete_response = client.delete(
        f"/api/v1/students/{student_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.get_json() == {
        "message": "Student deleted successfully"
    }

    get_response = client.get(
        f"/api/v1/students/{student_id}"
    )

    assert get_response.status_code == 404
    assert get_response.get_json() == {
        "error": "Student not found"
    }
def test_healthcheck():
    client = app.test_client()

    response = client.get("/healthcheck")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }
