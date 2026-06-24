# LINE Work Manager — FastAPI Backend (MVP)

A smart, stateful work management system operated entirely through a **LINE Bot** interface, integrated with **Google Gemini AI** for natural language understanding, **Railway PostgreSQL** for database storage, and **Google Calendar** for event/task synchronization.

---

## Key Features
1. **Interactive Conversational Flows**: Users can create projects, tasks, and events through step-by-step LINE questions, featuring Quick Reply button support.
2. **AI-Powered Parsing**: Integrates Google Gemini API to parse relative date/times (e.g., "tomorrow at 5pm", "this Friday at 3pm") and user reminder preferences.
3. **Full Calendar Sync**: Synchronizes tasks and events with Google Calendar instantly, configuring custom reminders/popups based on user choices.
4. **Offline/Dry-Run Support**: Runs seamlessly in mock mode if Google Calendar or LINE bot credentials are not yet configured, allowing painless local manual testing.
5. **Robust Architecture**: Organized using standard FastAPI routers, services, and models.

---

## Project Structure
```
Calendar/
├── main.py                  # FastAPI app entry point
├── webhook.py               # LINE Webhook handler (with simulated/mock POST mode)
├── routers/
│   ├── projects.py          # REST endpoints for Projects
│   ├── tasks.py             # REST endpoints for Tasks (CRUD + Calendar Sync)
│   └── events.py            # REST endpoints for Events (CRUD + Calendar Sync)
├── services/
│   ├── gemini_service.py    # Google Gemini API parser
│   ├── calendar_service.py  # Google Calendar integration (with dry-run support)
│   └── reminder_service.py  # Optional reminder scheduling logic
├── models/
│   ├── project.py           # Pydantic models for Projects
│   ├── task.py              # Pydantic models for Tasks
│   └── event.py             # Pydantic models for Events
├── session/
│   └── state_manager.py     # Stateful conversation machine
├── database.py              # PostgreSQL Client configuration (Railway-compatible)
├── config.py                # Environment variable loader
├── requirements.txt         # Package dependencies
└── README.md                # Documentation & SQL Setup Scripts
```

---

## PostgreSQL Database Schema Setup

Connect to your **Railway PostgreSQL** database using pgAdmin, psql, or the Railway Query Editor, and execute the following DDL statements to set up your tables:

```sql
-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Create Projects Table
CREATE TABLE public.projects (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL,
    user_id text NOT NULL,
    created_at timestamptz DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Create Tasks Table
CREATE TABLE public.tasks (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL,
    project_id uuid REFERENCES public.projects(id) ON DELETE CASCADE,
    deadline text NOT NULL,
    reminders jsonb DEFAULT '[]'::jsonb NOT NULL,
    calendar_event_id text,
    user_id text NOT NULL,
    created_at timestamptz DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Create Events Table
CREATE TABLE public.events (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL,
    start_time text NOT NULL,
    end_time text NOT NULL,
    location text,
    reminders jsonb DEFAULT '[]'::jsonb NOT NULL,
    calendar_event_id text,
    user_id text NOT NULL,
    created_at timestamptz DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Create Sessions Table (for LINE conversation states)
CREATE TABLE public.sessions (
    user_id text PRIMARY KEY,
    flow text,
    step text,
    partial_data jsonb DEFAULT '{}'::jsonb NOT NULL,
    updated_at timestamptz DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

---

## Getting Started

### 1. Installation
Install python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory (`Calendar/`) and populate your credentials:
```env
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:password@your_railway_host:port/railway
GOOGLE_CALENDAR_CREDENTIALS=your_google_service_account_json_content_or_path_to_json_file
```

*Note: If no credentials or `DATABASE_URL` are configured, the server will start up in dry-run/mock mode, allowing you to manually test the webhook routing immediately.*

### 3. Running the Server
Start the Uvicorn local server:
```bash
uvicorn main:app --reload
```
Open your browser and navigate to `http://localhost:8000/` to check the healthy status dashboard!

---

## Local Verification / Automated Testing

### Root Dashboard Check
Verify the service metadata and configuration statuses:
```bash
curl http://localhost:8000/
```

### Simulated Webhook Interaction
You can test the conversational state machine flow directly without a LINE client by sending simulated POST messages to `/webhook`:

**1. Hello (Main Menu)**
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"events": [{"source": {"userId": "user_abc"}, "message": {"text": "Hello"}}]}'
```

**2. Trigger Create Project Flow**
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"events": [{"source": {"userId": "user_abc"}, "message": {"text": "Create Project"}}]}'
```

**3. Cancel current flow**
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"events": [{"source": {"userId": "user_abc"}, "message": {"text": "cancel"}}]}'
```
