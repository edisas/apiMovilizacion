from fastapi import FastAPI
from routers import auth, user, upload

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(upload.router, prefix="/files", tags=["files"])


@app.get("/")
def root():
    return {"message": "Welcome to the API"}
