import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime

security = HTTPBearer()
SECRET_KEY = os.getenv("DEV_AGENT_JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"

class AuthService:
    """
    Shared JWT authentication service for agent ecosystem.
    """
    def __init__(self, secret: str = SECRET_KEY, algorithm: str = ALGORITHM):
        self.secret = secret
        self.algorithm = algorithm

    def validate_token(self, token: str) -> dict:
        """
        Validate and decode a JWT. Raises HTTPException for invalid/expired tokens.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm], options={"verify_aud": False})
            if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
                raise HTTPException(status_code=401, detail="Token expired")
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")

auth_service = AuthService()

async def validate_jwt(token = Depends(security)):
    """
    FastAPI dependency for JWT validation using AuthService.
    """
    return auth_service.validate_token(token.credentials)
