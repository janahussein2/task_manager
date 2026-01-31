from fastapi import FastAPI
from routers import users, tasks
from database import engine
from models import Base


app = FastAPI(title="Task Manager API", description="Full-stack Task Management System", version="1.0")


Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Task API 🚀"}

