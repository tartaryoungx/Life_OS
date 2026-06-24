from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import projects, tasks, events, test_calendar, webhook, login


app = FastAPI(
    title="LINE Work Manager API",
    description="Backend service for LINE Work Manager MVP, linking projects, tasks, and events to Google Calendar and Supabase.",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint
@app.get("/")
def read_root():
    return {
        "app": "LINE Work Manager API",
        "status": "healthy",
        "version": "1.0.0",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "line_configured": bool(settings.LINE_CHANNEL_ACCESS_TOKEN and settings.LINE_CHANNEL_SECRET),
        "supabase_configured": bool(settings.DATABASE_URL),
        "google_calendar_configured": bool(settings.GOOGLE_CALENDAR_CREDENTIALS)
    }

# Include routers
app.include_router(webhook.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(test_calendar.router)
app.include_router(login.router)

if __name__ == "__main__":
    import uvicorn
    # Run server locally
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
