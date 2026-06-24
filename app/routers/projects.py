from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.database import get_db
from app.models.project import ProjectCreate

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", status_code=201)
def create_project(project: ProjectCreate):
    db = get_db()
    try:
        res = db.table("projects").insert({
            "name": project.name,
            "user_id": project.user_id
        }).execute()
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create project.")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_projects(user_id: str):
    db = get_db()
    try:
        res = db.table("projects").select("*").eq("user_id", user_id).execute()
        return res.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
