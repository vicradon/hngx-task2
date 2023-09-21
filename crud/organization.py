from sqlalchemy.orm import Session
from db import models, schemas


def get_organization(db: Session, organization_id: int):
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()


def create_organization(db: Session, organization: schemas.OrganizationCreate):
    db_organization = models.Organization(name=organization.name, lunch_price=organization.lunch_price)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

