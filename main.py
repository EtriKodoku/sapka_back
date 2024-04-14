from app import app
import uvicorn
from config import CONFIG


if __name__ == "__main__":
    uvicorn.run(app="app:app", reload=True, ssl_certfile=CONFIG.ssl_certfile, ssl_keyfile=CONFIG.ssl_keyfile)
