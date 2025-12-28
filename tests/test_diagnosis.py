import pytest


@pytest.fixture
def authenticated_client(client, test_user_data):
    """Get authenticated client"""
    client.post("/api/v1/auth/register", json=test_user_data)
    response = client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = response.json()["data"]["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


def test_check_symptoms(authenticated_client):
    """Test symptom checking"""
    response = authenticated_client.post("/api/v1/diagnosis/check", json={
        "symptoms": ["dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "disease" in data["data"]
    assert "confidence" in data["data"]


def test_get_diagnosis_history(authenticated_client):
    """Test getting diagnosis history"""
    # First create a diagnosis
    authenticated_client.post("/api/v1/diagnosis/check", json={
        "symptoms": ["white_powdery_coating", "distorted_leaves"]
    })
    
    # Then get history
    response = authenticated_client.get("/api/v1/diagnosis/history")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] > 0


def test_get_available_symptoms(authenticated_client):
    """Test getting available symptoms"""
    response = authenticated_client.get("/api/v1/diagnosis/symptoms")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0