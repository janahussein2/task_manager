from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from models import Task, User
from database import SessionLocal
from schemas.models import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    return query.all()

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # تحقق من إن assigned_to موجود في users
    if task.assigned_to:
        user = db.query(User).filter(User.id == task.assigned_to).first()
        if not user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        assigned_to=task.assigned_to
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status_update: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status_update
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully", "task_id": task_id}

