from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_headers
import secrets
import time

mcp = FastMCP("AuthLab Username Password Demo")

#pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ideally users will be in db
USERS = {
    "admin": "admin",
    "user": "user",
}

SESSION_TTL_SECONDS = 60 * 60 # 1hour

SESSIONS: dict[str, dict] = {}

def issue_token(username: str) -> str | None:
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user": username,
        "exp": SESSION_TTL_SECONDS,
    }
    return token

def validate_token(token: str) -> str | None:
    session = SESSIONS.get(token)
    if not session:
        return None
    if session["exp"] < time.time():
        return None
    return session["user"]
    


# Bad idea
@mcp.tool()
def auth_login(username: str, password: str):
    stored_password = USERS.get(username)
    if not stored_password:
        raise PermissionError("Invalid username or password")
    if stored_password != password :
        raise PermissionError("Invalid username or password")
    return {
        "session_token": issue_token(username),
        "token_type": "Bearer",
        "expires_in": SESSION_TTL_SECONDS
    }




@mcp.middleware
async def auth_middleware(ctx: Context, call_next):
    headers = get_http_headers()
    auth = headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        token = auth.split(" ")[1].strip()
        username = validate_token(token)
        if username:
            ctx.set_state("username", username)
            
    return await call_next(ctx)


@mcp.tool()
def whoami(ctx: Context):
    user = ctx.get_state("username")
    if not user:
        raise PermissionError("Not logged in")
    return user
