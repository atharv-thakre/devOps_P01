from authlib.integrations.starlette_client import OAuth
from fastapi import  Request , APIRouter
from fastapi.responses import RedirectResponse
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URL


router = APIRouter(prefix="/auth", tags=["auth"])
oauth = OAuth()


oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@router.get("/login/google")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    print("CLIENT:", GOOGLE_CLIENT_ID)
    print("CALLBACK:", redirect_uri)

    print(response.headers["location"])

    return response

@router.get("/callback", name="callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]

    # Find/create user
    jwt = "your_jwt_token_here"  

    response = RedirectResponse(REDIRECT_URL)

    response.set_cookie(
        key="access_token",
        value=jwt,
        httponly=True,
        secure=False,  # Set to True in production
        samesite="lax"
    )

    return response



