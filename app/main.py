from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

# Create tables in MySQL (for dev; in prod you'd use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/items/", response_model=schemas.ItemRead)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    db_item = models.Item(
        name=item.name,
        price=item.price,
        is_offer=item.is_offer or False,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=schemas.ItemRead)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=List[schemas.ItemRead])
def list_items(
    db: Session = Depends(get_db),
):
    items = db.query(models.Item).all()
    return items

@app.put("/items/{item_id}", response_model=schemas.ItemRead)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.price = item.price
    db_item.is_offer = item.is_offer or False

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted", "item_id": item_id}
