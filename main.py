"""
This module sets up a FastAPI application with JWT authentication and Prisma ORM integration.

It includes configurations for development and production environments, JWT token verification,
and the initialization of the Prisma client.
"""

import json
import io
import sys
import pytest
from functools import lru_cache
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Optional
from config import Settings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime
from prisma import Prisma
from fastapi.middleware.cors import CORSMiddleware


# Instantiate Settings directly
settings = Settings()

if settings.env.lower() == "dev":
    print("Running in dev mode")
    app = FastAPI(debug=True)
else:
    app = FastAPI(openapi_url=None, debug=False)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Prisma client
prisma = Prisma()

# JWT Configuration
SECRET_KEY = settings.auth_secret  # Should match your frontend secret
ALGORITHM = "HS256"

# OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    """
    TokenData is used to parse and validate the username information from the JWT token.
    """

    username: Optional[str] = None


# Function to verify the token
async def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("userId")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"userId": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "env": settings.env,
        "app_name": settings.app_name,
    }


@app.post("/tests/{test_id}/run")
async def run_test(test_id: str, user_data: Annotated[dict, Depends(decode_token)]):
    # print(f"Received request for user: {user_data}, test_id: {test_id}")
    test_data = await prisma.test.find_unique(where={"id": test_id})

    test_data_dict = test_data.dict()
    prepared_test_data = {
        "base_url": test_data_dict["baseUrl"],
        "steps": await prisma.step.find_many(
            where={"testId": test_id}, order={"order": "asc"}
        ),
    }
    # test_data = None
    # for doc in query:
    #     test_data = doc.to_dict()
    #     break

    # if not test_data:
    #     return jsonable_encoder({"error": "Test not found"}), 404

    # # Run the test
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        pytest.main(
            [
                "-x",
                "WebTest/Test/test_web.py::test_login",
                "-vv",
                "--test_data",
                json.dumps(prepared_test_data),
            ]
        )
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    stdout_output = stdout.getvalue()
    stderr_output = stderr.getvalue()

    # return jsonable_encoder({"stdout": stdout_output, "stderr": stderr_output}), 200
    return {"message": "Test run successful"}


# Startup event to connect to the database
@app.on_event("startup")
async def startup():
    await prisma.connect()


# Shutdown event to disconnect from the database
@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
