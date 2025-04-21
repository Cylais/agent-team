from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def validate_jwt(token = Depends(security)):
    # Simplified validation logic
    if not token.credentials.startswith("valid_jwt"):
        raise HTTPException(status_code=403, detail="Invalid credentials")
