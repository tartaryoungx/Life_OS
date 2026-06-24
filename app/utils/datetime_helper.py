from datetime import datetime, timedelta


def day_quick_replies():
    return [
        "Today",
        "Tomorrow",
        "Next 2 day",
        "Next week",
        "Custom date",
        "Cancel",
    ]


def time_quick_replies():
    return [
        "09:00",
        "12:00",
        "17:00",
        "20:00",
        "Custom time",
        "Cancel",
    ]

def reminder_quick_replies():
    return [
        "15 minutes before",
        "1 hour before",
        "1 day before",
        "3 days before",
        "No reminder",
        "Cancel",
    ]

def parse_day(text_clean):
    today = datetime.now().date()
    text = text_clean.strip().lower()

    if text == "today":
        return today
    if text == "tomorrow":
        return today + timedelta(days=1)
    if text in ["next 2 day", "next 2 days"]:
        return today + timedelta(days=2)
    if text == "next week":
        return today + timedelta(days=7)

    try:
        return datetime.strptime(text_clean.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def parse_time(text_clean):
    try:
        return datetime.strptime(text_clean.strip(), "%H:%M").time()
    except ValueError:
        return None
    
def parse_reminders(text_clean):
    text = text_clean.strip().lower()

    if text == "no reminder":
        return None

    allowed = {
        "15 minutes before": "15 minutes before",
        "1 hour before": "1 hour before",
        "1 day before": "1 day before",
        "3 days before": "3 days before",
    }

    return [allowed[text]] if text in allowed else None

