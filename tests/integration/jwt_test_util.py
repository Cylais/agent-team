import os
import time
from jose import jwt

SECRET_KEY = os.getenv("DEV_AGENT_JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"

def make_test_jwt(sub="test-user", exp=None, extra=None):
    if exp is None:
        exp = int(time.time()) + 3600  # 1 hour from now
    payload = {"sub": sub, "exp": exp}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
