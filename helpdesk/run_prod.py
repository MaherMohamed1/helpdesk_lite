import os
from waitress import serve
from server.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting production server on {host}:{port}")
    serve(app, host=host, port=port)
