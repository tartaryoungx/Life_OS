import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path so imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root_endpoint():
    """
    Test that the root endpoint is reachable and returns health status.
    """
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["app"] == "LINE Work Manager API"
    assert json_data["status"] == "healthy"

def test_webhook_simulated_menu_flow():
    """
    Test the simulated webhook flow when starting from scratch.
    """
    # Send a message "Hello" to start and trigger the main menu
    payload = {
        "events": [
            {
                "source": {"userId": "test_user_123"},
                "message": {"text": "Hello"}
            }
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    
    assert json_data["status"] == "simulated"
    result = json_data["results"][0]
    assert result["userId"] == "test_user_123"
    assert "Welcome to LINE Work Manager" in result["response"]["reply_text"]
    assert "Create Project" in result["response"]["quick_replies"]

def test_webhook_simulated_create_project_trigger():
    """
    Test triggering the Create Project flow.
    """
    payload = {
        "events": [
            {
                "source": {"userId": "test_user_123"},
                "message": {"text": "Create Project"}
            }
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    
    result = json_data["results"][0]
    assert "Project Name?" in result["response"]["reply_text"]

def test_webhook_simulated_cancel():
    """
    Test that typing cancel resets the state.
    """
    payload = {
        "events": [
            {
                "source": {"userId": "test_user_123"},
                "message": {"text": "cancel"}
            }
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    
    result = json_data["results"][0]
    assert "cancelled" in result["response"]["reply_text"]
