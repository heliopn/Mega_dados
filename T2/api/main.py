# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from .models import Task
from .routers import task


tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)



app.include_router(
    task.router,
    prefix="/task",
    tags=["task"],
    responses={404: {"description": "Not found"}},
)



