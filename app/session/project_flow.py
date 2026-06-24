from typing import Dict, Any
from app.database import get_db

def handle_project_flow(cls, user_id, text_clean, step):
    if step == cls.STEP_P_NAME:
        project_name = text_clean
        db = get_db()
        try:
            # Save Project
            db.table("projects").insert({
                "name": project_name,
                "user_id": user_id
            }).execute()
            
            cls.clear_session(user_id)
            return {
                "reply_text": f"Project created successfully: {project_name}",
                "quick_replies": ["Create Task", "Create Event", "Create Project"]
            }
        except Exception as e:
            print(f"Error saving project: {e}")
            cls.clear_session(user_id)
            return {
                "reply_text": f"Error saving project. Please try again later. Details: {str(e)}",
                "quick_replies": ["Create Task", "Create Event", "Create Project"]
            }
