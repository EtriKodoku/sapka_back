from fastapi import FastAPI
from config import CONFIG
from routers import auth, ai
from fastsession import FastSessionMiddleware, MemoryStore

app = FastAPI(debug=CONFIG.DEBUG)

app.include_router(auth.router)
app.include_router(ai.router)

app.add_middleware(FastSessionMiddleware,
                   secret_key="my-secret-key",  # Key for cookie signature
                   store=MemoryStore(),  # Store for session saving
                   http_only=True,  # True: Cookie cannot be accessed from client-side scripts such as JavaScript
                   secure=False,  # True: Requires Https
                   max_age=0,
                   # When 0 is specified, it is only effective while the browser is active. If a value greater than 0 is specified, the session will continue for the specified time even after closing the browser
                   session_cookie="sid",  # Name of the session cookie
                   session_object="session"  # Attribute name of the Session manager under request.state
)