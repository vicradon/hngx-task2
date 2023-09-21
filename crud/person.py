from sqlalchemy.orm import Session
from db import models, schemas


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def get_person_by_email(db: Session, email: str):
    return db.query(models.Person).filter(models.Person.email == email).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id=person_id)
    db.delete(db_person)
    db.commit()
    return {"status": "success", "message": "successfully delete person"}

def update_person_details(db: Session, person_id: int, updated_details: schemas.PersonCreate):
    db_person = get_person(db, person_id)

    db_person.first_name = updated_details.first_name
    db_person.last_name = updated_details.last_name
    db_person.email = updated_details.email

    db.commit()
    db.refresh(db_person)
    return db_person

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(email=person.email, first_name=person.first_name, last_name=person.last_name, organization_id=person.organization_id)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

