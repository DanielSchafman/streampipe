from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Steampipe API"}

