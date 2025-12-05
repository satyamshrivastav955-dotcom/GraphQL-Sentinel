import yaml
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes, gateway

app = FastAPI(title="GraphQL Sentinel", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_config():
    with open("backend/config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def load_model_paths():
    with open("backend/config/model_paths.json", "r") as f:
        return json.load(f)

@app.on_event("startup")
async def startup_event():
    config = load_config()
    model_paths = load_model_paths()
    
    # Initialize gateway
    routes.gateway = gateway.GraphQLGateway(config, model_paths)
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(config['logging']['save_path']), exist_ok=True)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
