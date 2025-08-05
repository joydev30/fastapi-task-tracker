from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder

app = FastAPI()
class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
tasks = {}

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

@app.get("/")
def read_root():
    return {"message": "Hello, world"}

@app.get("/tasks")
def get_tasks(completed: Optional[bool] = None):
    if completed is None:
        return list(tasks.values())
    return [task for task in tasks.values() if task.completed == completed]

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    if task.id in tasks:
        return HTTPException(status_code=400, detail="Task with this ID already exists.")
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    tasks[task.id] = task
    return task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks.pop(task_id)
    return deleted_task

@app.patch("/tasks/{task_id}")
def partial_update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    stored_task_data = tasks[task_id].dict()
    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        stored_task_data[field] = value
    tasks[task_id] = Task(**stored_task_data)
    return tasks[task_id]