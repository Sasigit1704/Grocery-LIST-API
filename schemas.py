from pydantic import BaseModel
from typing import Optional
class Item(BaseModel):
    id: int
    name: str
    quantity: int
class ItemUpdate(BaseModel):
    name: str
    quantity: int
class ItemPatch(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None