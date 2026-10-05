import yaml
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes, gateway

DEFAULT_CONFIG = {
    "logging": {"save_path": "backend/storage/logs/decisions.jsonl"},
    "cors": {"allow_origins": ["http://localhost:5173", "http://localhost:3000"]},
}

def load_config():
    with open("backend/config/settings.yaml", "r") as f:
        return yaml.safe_load(f) or {}

def load_model_paths():
    if not os.path.exists("backend/config/model_paths.json"):
        return {}
    with open("backend/config/model_paths.json", "r") as f:
        return json.load(f)

app = FastAPI(title="GraphQL Sentinel", version="1.0.0")

# CORS — origins are configurable via settings.yaml (never wildcard-with-credentials)
_config = load_config() if os.path.exists("backend/config/settings.yaml") else DEFAULT_CONFIG
_cors_config = _config.get("cors") or DEFAULT_CONFIG["cors"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_config.get("allow_origins", DEFAULT_CONFIG["cors"]["allow_origins"]),
    allow_credentials=bool(_cors_config.get("allow_credentials", True)),
    allow_methods=_cors_config.get("allow_methods", ["*"]),
    allow_headers=_cors_config.get("allow_headers", ["*"]),
)

@app.on_event("startup")
async def startup_event():
    config = _config or load_config()
    model_paths = load_model_paths()

    # Initialize gateway
    routes.gateway = gateway.GraphQLGateway(config, model_paths)

    # Ensure log directory exists
    save_path = config.get("logging", {}).get(
        "save_path", DEFAULT_CONFIG["logging"]["save_path"]
    )
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
