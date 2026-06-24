from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["Login"])

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_SECRET = "client_secret.json"
REDIRECT_URI = "http://localhost:8000/auth/callback"

@router.get("/login")
def login():

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=False,
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )

    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(code: str):

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=False,
    )

    flow.fetch_token(code=code)

    creds = flow.credentials


    with open("token.json", "w") as f:
        f.write(creds.to_json())

    return {"ok": True}