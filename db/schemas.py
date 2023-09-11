from typing import List, Union
from pydantic import BaseModel

class PersonBase(BaseModel):
    email: str
    first_name: str 
    last_name: str 

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        orm_mode = True
