from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_environment import AppEnvironment
from env import env
from controllers import ticket

# Create app
app = FastAPI(
    title="Kiros Triage API",
    debug=env.DEBUG
)

# CORS
if AppEnvironment.is_local_env(env.APP_ENV):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(ticket.router, prefix="/api")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}