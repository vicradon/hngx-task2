import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List
import os
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from crud.person import create_person, get_person_by_email, get_person, get_persons, update_person_details, delete_person
from crud.organization import create_organization, get_organization, get_organizations
from db import schemas, models
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return RedirectResponse("/docs")


@app.post('/organization', response_model=schemas.Organization)
def create_organization_handler(organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    return create_organization(db=db, organization=organization)


@app.get('/api', response_model=List[schemas.Person])
def fetch_persons_handler(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = get_persons(db, skip=skip, limit=limit)
    return persons

@app.get('/api/{person_id}', response_model=schemas.Person)
def fetch_person_handler(person_id: int, db: Session = Depends(get_db)):
    db_person = get_person(db, person_id=person_id)

    if not(db_person):
        raise HTTPException(status_code=404, detail="Person with this id does not exist")

    return db_person

@app.post('/api', response_model=schemas.Person)
def create_person_handler(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = get_person_by_email(db, email=person.email)

    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_person(db=db, person=person)

@app.patch('/api/{person_id}')
def update_person_handler(person_id: int, updated_details: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = get_person(db, person_id=person_id)
    user_with_email = get_person_by_email(db, email=updated_details.email)

    if not(db_person):
        raise HTTPException(status_code=404, detail="Person with this id does not exist")

    if user_with_email:
        raise HTTPException(status_code=400, detail="This email is already in use")

    return update_person_details(db, person_id=person_id, updated_details=updated_details)

@app.delete('/api/{person_id}')
def delete_person_handler(person_id: int, db: Session = Depends(get_db)):
    db_person = get_person(db, person_id=person_id)

    if not(db_person):
        raise HTTPException(status_code=404, detail="Person with this id does not exist")

    delete_person(db, person_id=person_id)
    return {"status": "success", "message": "successfully delete person"}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", port=port, log_level="info", reload=True)