# import libraries
from fastapi import FastAPI
from api.routes_user import router as user_router
import uvicorn

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
