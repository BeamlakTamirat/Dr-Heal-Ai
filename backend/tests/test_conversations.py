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


@pytest.fixture
def auth_token():
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )
    return response.json()["access_token"]


class TestConversations:
    
    def test_get_conversations_empty(self, auth_token):
        response = client.get(
            "/api/conversations",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_conversations_unauthorized(self):
        response = client.get("/api/conversations")
        assert response.status_code == 403
    
    def test_chat_create_conversation(self, auth_token):
        response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": "I have a headache"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "message_id" in data
        assert "response" in data
        assert "agent_used" in data
    
    def test_chat_continue_conversation(self, auth_token):
        first_response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": "I have a headache"}
        )
        conversation_id = first_response.json()["conversation_id"]
        
        second_response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "conversation_id": conversation_id,
                "query": "What should I do?"
            }
        )
        assert second_response.status_code == 200
        assert second_response.json()["conversation_id"] == conversation_id
    
    def test_chat_empty_query(self, auth_token):
        response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": ""}
        )
        assert response.status_code == 422
    
    def test_chat_long_query(self, auth_token):
        long_query = "a" * 1001 
        response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": long_query}
        )
        assert response.status_code == 422
    
    def test_get_conversation_detail(self, auth_token):
        chat_response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": "I have a fever"}
        )
        conversation_id = chat_response.json()["conversation_id"]
        
        response = client.get(
            f"/api/conversations/{conversation_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conversation_id
        assert "messages" in data
        assert len(data["messages"]) == 2
    
    def test_get_nonexistent_conversation(self, auth_token):
        response = client.get(
            "/api/conversations/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 404
    
    def test_delete_conversation(self, auth_token):
        chat_response = client.post(
            "/api/conversations/chat",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"query": "Test message"}
        )
        conversation_id = chat_response.json()["conversation_id"]
        
        response = client.delete(
            f"/api/conversations/{conversation_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 204
        
        get_response = client.get(
            f"/api/conversations/{conversation_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == 404
    
    def test_list_conversations(self, auth_token):
        for i in range(3):
            client.post(
                "/api/conversations/chat",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={"query": f"Test message {i}"}
            )
        
        response = client.get(
            "/api/conversations",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in conv for conv in data)
        assert all("title" in conv for conv in data)
        assert all("message_count" in conv for conv in data)
