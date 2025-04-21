from fastapi import FastAPI
from ux_agent.api import ux_router
from ux_agent.security import validate_jwt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(ux_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
