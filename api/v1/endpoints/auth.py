from fastapi import APIRouter
import jwt
import datetime

router = APIRouter()

SECRET_KEY = "dev-secret"
ALGORITHM = "HS256"

@router.post("/login")
async def login(username: str):
    payload = {
        "user_id": username,
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
