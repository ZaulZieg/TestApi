from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True  # tells Pydantic it can read from ORM objects
