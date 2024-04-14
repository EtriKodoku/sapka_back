from app import app
import uvicorn
from config import CONFIG


if __name__ == "__main__":
    print(CONFIG.ssl_certfile, CONFIG.ssl_keyfile)
    uvicorn.run(app="app:app", host="0.0.0.0", port=433, reload=True, ssl_keyfile=CONFIG.ssl_keyfile, ssl_certfile=CONFIG.ssl_certfile)
