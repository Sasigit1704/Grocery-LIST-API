from pydantic import BaseModel, Field
from typing import Optional

class GroceryList(BaseModel):
    listId: int
    listName: str
    
class Item(BaseModel):
    id: int = Field(..., ge=1, le=9999, description="Item ID must be between 1 and 9999")
    name: str = Field(..., min_length=2, max_length=50, description="Item name length between 2 and 50 characters")
    quantity: int = Field(..., ge=1, le=1000, description="Quantity must be between 1 and 1000")

class ItemUpdate(BaseModel):
    id: int = Field(..., ge=1, le=9999)
    name: str = Field(..., min_length=2, max_length=50)
    quantity: int = Field(..., ge=1, le=1000)

class ItemPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    quantity: Optional[int] = Field(None, ge=1, le=1000)