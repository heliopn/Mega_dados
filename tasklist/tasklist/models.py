# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

#Trabalhamos com inclusão total das pessoas, por isso nosso max_length consegue aceitar
#até mesmo o nome de pessoa mais longo do mundo e sobram alguns caracteres.
class User(BaseModel):
    username: str = Field(
        'Somebody That I Used to Know',
        title='Username',
        max_length=1060,
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "Mr.Robot",
            }
        }

# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )
    task_owner: str = Field(
        title="Task Owner",
        max_length=1024,
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Hack the box!',
                'completed': False,
                "task_owner": "bd65600d-8669-4903-8a14-af88203add38",
            }
        }


