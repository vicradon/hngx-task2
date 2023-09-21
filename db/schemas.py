from typing import List, Union
from pydantic import BaseModel

class PersonBase(BaseModel):
    email: str
    first_name: str 
    last_name: str 
    organization_id: int

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    name: str
    lunch_price: int 

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    persons: List[Person] = []

    class Config:
        orm_mode = True
