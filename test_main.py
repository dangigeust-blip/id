from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Positive Test Cases

def test_valid_student_registration():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "919876543210",
        "email": "rahul101@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Student registered successfully"
    assert response.json()["unique_id"].startswith("AIM-")


def test_another_student_registration():
    response = client.post("/register", json={
        "student_name": "Amit",
        "mobile_no": "919876543211",
        "email": "amit101@gmail.com",
        "course": "BSc"
    })

    assert response.status_code == 200


# Negative Test Cases

def test_name_with_numbers():
    response = client.post("/register", json={
        "student_name": "Rahul123",
        "mobile_no": "919876543210",
        "email": "rahul102@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_name_with_special_characters():
    response = client.post("/register", json={
        "student_name": "Rahul@",
        "mobile_no": "919876543210",
        "email": "rahul103@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_name_with_spaces():
    response = client.post("/register", json={
        "student_name": "Rahul Kumar",
        "mobile_no": "919876543210",
        "email": "rahul104@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_mobile_less_than_12_digits():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "91987654321",
        "email": "rahul105@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_mobile_more_than_12_digits():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "9198765432101",
        "email": "rahul106@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_mobile_without_91():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "819876543210",
        "email": "rahul107@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_mobile_with_alphabets():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "91ABC1234567",
        "email": "rahul108@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_invalid_email():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "919876543210",
        "email": "rahulgmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_missing_student_name():
    response = client.post("/register", json={
        "mobile_no": "919876543210",
        "email": "rahul109@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_missing_mobile_number():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "email": "rahul110@gmail.com",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_missing_email():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "919876543210",
        "course": "BCA"
    })

    assert response.status_code == 422


def test_missing_course():
    response = client.post("/register", json={
        "student_name": "Rahul",
        "mobile_no": "919876543210",
        "email": "rahul111@gmail.com"
    })

    assert response.status_code == 422
