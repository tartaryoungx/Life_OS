import json
from datetime import datetime
from typing import Dict, Any
from app.database import get_db
from app.session.task_flow import handle_task_flow
from app.session.event_flow import handle_event_flow
from app.session.project_flow import handle_project_flow

class StateManager:
    # Flows
    FLOW_PROJECT = "create_project"
    FLOW_TASK = "create_task"
    FLOW_EVENT = "create_event"

    # Steps for Project
    STEP_P_NAME = "ASK_PROJECT_NAME"

    # Steps for Task
    STEP_T_NAME = "ASK_TASK_NAME"
    STEP_T_PROJECT = "ASK_LINKED_PROJECT"
    STEP_T_DEADLINE_DAY = "ASK_DEADLINE_DAY"
    STEP_T_DEADLINE_TIME = "ASK_DEADLINE_TIME"
    STEP_T_REMINDER = "ASK_TASK_REMINDER"

    # Steps for Event
    STEP_E_NAME = "ASK_EVENT_NAME"
    STEP_E_DATE = "ASK_EVENT_DATE"
    STEP_E_TIME = "ASK_EVENT_TIME"
    STEP_E_REMINDER = "ASK_EVENT_REMINDER"

    @classmethod
    def handle_message(cls, user_id: str, user_input: str) -> Dict[str, Any]:

        text_clean = user_input.strip()
        
        # Support session cancellation
        if text_clean.lower() in ["cancel", "reset", "ยกเลิก", "main menu"]:
            return cls.clear_session(user_id)

        #If user don't have a session create the new one, else continue
        session = cls.get_or_create_session(user_id)
        flow = session.get("flow")
        step = session.get("step")
        partial_data = cls.parse_partial_data(session)

        # ----------------------------------------------------
        # MAIN MENU / INITIAL FLOW SELECTION
        # ----------------------------------------------------
        if not flow:
            return cls.handle_main_menu(
                user_id = user_id, 
                text_clean = text_clean,
            )

        # ----------------------------------------------------
        # FLOW: CREATE PROJECT
        # ----------------------------------------------------
        if flow == cls.FLOW_PROJECT:
            return handle_project_flow(
                cls,
                user_id = user_id,
                text_clean = text_clean,
                step = step,
            )

        # ----------------------------------------------------
        # FLOW: CREATE TASK
        # ----------------------------------------------------
        elif flow == cls.FLOW_TASK:
            return handle_task_flow(
                cls,
                user_id = user_id,
                text_clean = text_clean,
                step = step,
                partial_data = partial_data,
            )

        # ----------------------------------------------------
        # FLOW: CREATE EVENT
        # ----------------------------------------------------
        elif flow == cls.FLOW_EVENT:
            return handle_event_flow(
                cls,
                user_id = user_id,
                text_clean = text_clean,
                step = step,
                partial_data = partial_data,
            )

        # Fallback if something went wild
        cls.clear_session(user_id)
        return {
            "reply_text": "An error occurred with your session state. Resetting to main menu.",
            "quick_replies": ["Create Project", "Create Task", "Create Event"]
        }
    
    @classmethod
    def get_or_create_session(cls, user_id: str) -> Dict[str, Any]:
        #Retrieves the session from Supabase, or creates a new idle one.
        db = get_db()
        try:
            res = db.table("sessions").select("*").eq("user_id", user_id).execute()
            if res.data and len(res.data) > 0:
                return res.data[0] 
            
            # Create idle session
            new_session = cls.idle_session(user_id)
            db.table("sessions").insert(new_session).execute()
            return new_session
    
        except Exception as e:
            print(f"Error accessing session for {user_id}: {e}.")
            return cls.idle_session(user_id)
    
    @classmethod
    def update_session(cls, user_id: str, flow: str | None = None, step: str | None = None, partial_data: Dict[str, Any] | None = None):
        """
        Updates session state in Supabase.
        """
        db = get_db()
        try:
            db.table("sessions").upsert({
                "user_id": user_id,
                "flow": flow,
                "step": step,
                "partial_data": partial_data,
                "updated_at": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error updating session for {user_id}: {e}")
        
    @classmethod
    def clear_session(cls, user_id: str):
        """
        Resets session state to idle.
        """
        cls.update_session(user_id, None, None, {})
        return {
                "reply_text": "Hello! Welcome to LINE Work Manager. Please select an option from the menu:\n\n1. Create Project\n2. Create Task\n3. Create Event",
                "quick_replies": ["Create Task", "Create Event", "Create Project"]
            }
    
    @staticmethod
    def parse_partial_data(session):
        # Handle parsed json string or actual dict
        partial_data = session.get("partial_data") or {}
        if isinstance(partial_data, str):
            try:
                partial_data = json.loads(partial_data)
            except Exception:
                partial_data = {}
        return partial_data
    
    # ----------------------------------------------------
    # MAIN MENU / INITIAL FLOW SELECTION
    # ----------------------------------------------------    
    @classmethod
    def handle_main_menu(cls, user_id, text_clean):
        if text_clean in ["Create Project", "สร้างโปรเจกต์", "1"]:
            cls.update_session(user_id, cls.FLOW_PROJECT, cls.STEP_P_NAME, {})
            return {
                "reply_text": "Project Name?",
                "quick_replies": ["Project Name","cancel"]
            }
        elif text_clean in ["Create Task", "สร้างงาน", "2"]:
            cls.update_session(user_id, cls.FLOW_TASK, cls.STEP_T_NAME, {})
            return {
                "reply_text": "Task Name?",
                "quick_replies": ["Task Name","cancel"]
            }
        elif text_clean in ["Create Event", "สร้างอีเวนต์", "3"]:
            cls.update_session(user_id, cls.FLOW_EVENT, cls.STEP_E_NAME, {})
            return {
                "reply_text": "Event Name?",
                "quick_replies": ["Event Name","cancel"]
            }
        else:
            return {
                "reply_text": "Resetting to main menu.\nHello! Welcome to LINE Work Manager. Please select an option from the menu:\n\n1. Create Project\n2. Create Task\n3. Create Event",
                "quick_replies": ["Create Project", "Create Task", "Create Event"]
            }        
    @staticmethod
    def idle_session(user_id):
        return {
            "user_id": user_id,
            "flow": None,
            "step": None,
            "partial_data": {}
        }