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
from fastapi import Depends, FastAPI, HTTPException, status, Body
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

@app.post("/tests/run_multiple")
async def run_multiple_tests(
    test_ids: Annotated[list[str], Body(...)],
    user_data: Annotated[dict, Depends(decode_token)],
):
    all_prepared_test_data = []
    results = []
    for test_id in test_ids:
        try:
            test_data = await prisma.test.find_unique(where={"id": test_id})

            if not test_data:
                raise HTTPException(status_code=404, detail="Test not found")

            test_data_dict = jsonable_encoder(test_data)
            steps = await prisma.step.find_many(
                where={"testId": test_id}, order={"order": "asc"}
            )

            if not steps:
                raise HTTPException(status_code=400, detail="No steps found for this test")

            prepared_test_data = {
                "base_url": test_data_dict["baseUrl"],
                "steps": jsonable_encoder(steps),
                "test_id": test_id,  # Include the test_id in the prepared data
            }
            all_prepared_test_data.append(prepared_test_data)

        except HTTPException as e:
            # Handle errors for individual tests if needed
            pass  # Or you can collect errors and return them in the response

    # Now, send all the prepared test data to pytest at once
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        pytest.main(
            [
                "-x",
                "WebTest/Test/test_web.py::test_login",  # Adjust if tests are in different files
                "-vv",
                "--test_data",
                json.dumps(all_prepared_test_data),  # Send all test data
            ]
        )

        stdout_output = stdout.getvalue()
        stderr_output = stderr.getvalue()

        # Assuming your pytest output provides information about individual test results
        # You'll need to parse the output to extract results for each test_id

        # Example: If pytest output contains lines like "test_id: <test_id>, status: <status>, message: <message>"
        for line in stdout_output.splitlines():
            if line.startswith("test_id:"):
                parts = line.split(", ")
                test_id = parts[0].split(": ")[1]
                status = parts[1].split(": ")[1]
                message = parts[2].split(": ")[1]
                results.append({
                    "test_id": test_id,
                    "status": status,
                    "message": message,
                })

    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    return results
    
    

@app.post("/tests/{test_id}/run")
async def run_test(test_id: str, user_data: Annotated[dict, Depends(decode_token)]):
    # print(f"Received request for user: {user_data}, test_id: {test_id}")
    test_data = await prisma.test.find_unique(where={"id": test_id})

    if not test_data:
        raise HTTPException(status_code=404, detail="Test not found")

    test_data_dict = jsonable_encoder(test_data)
    steps = await prisma.step.find_many(
        where={"testId": test_id}, order={"order": "asc"}
    )

    if not steps:
        raise HTTPException(status_code=400, detail="No steps found for this test")

    prepared_test_data = {
        "base_url": test_data_dict["baseUrl"],
        "steps": jsonable_encoder(steps),
    }

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
    return {
        "message": "Test run successful",
        "stdout": stdout_output,
        "stderr": stderr_output,
    }


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
