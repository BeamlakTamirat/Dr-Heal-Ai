
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.database import Base
from app.database.connection import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAuthentication:
    
    def test_register_success(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["name"] == "Test User"
    
    def test_register_duplicate_email(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password456",
                "name": "Another User"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "name": "Test User"
            }
        )
        assert response.status_code == 422
    
    def test_register_short_password(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
                "name": "Test User"
            }
        )
        assert response.status_code == 422
    
    def test_login_success(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_login_wrong_password(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user(self):
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        token = register_response.json()["access_token"]
        
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
    
    def test_get_current_user_no_token(self):
        response = client.get("/api/auth/me")
        assert response.status_code == 403
    
    def test_get_current_user_invalid_token(self):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_update_profile(self):
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            }
        )
        token = register_response.json()["access_token"]
        
        response = client.put(
            "/api/auth/me?name=Updated Name",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
