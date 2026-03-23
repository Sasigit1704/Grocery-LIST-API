from pydantic import BaseModel, Field
from typing import Optional


class GroceryList(BaseModel):
    listName: str = Field(..., min_length=2, max_length=50)


class Item(BaseModel):
    id: int = Field(..., ge=1, le=9999)
    name: str = Field(..., min_length=2, max_length=50)
    quantity: int = Field(..., ge=1, le=1000)


class ItemPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    quantity: Optional[int] = Field(None, ge=1, le=1000)