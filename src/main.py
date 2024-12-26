import uvicorn
from fastapi import FastAPI

from src.api import wallet_router

app = FastAPI()

app.include_router(wallet_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080)
