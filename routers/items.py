from fastapi import APIRouter, HTTPException, Depends
from schemas import Item, ItemPatch
from services.database import get_db
from services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])


def get_service(db=Depends(get_db)):
    return ItemService(db)


@router.get("/{list_id}")
def get_items(list_id: str, service=Depends(get_service)):

    items = service.get_items(list_id)

    if items is None:
        raise HTTPException(status_code=404, detail="List not found")

    return items


@router.post("/{list_id}")
def add_item(list_id: str, item: Item, service=Depends(get_service)):

    result = service.add_item(list_id, item)

    if result == "INVALID_ID":
        raise HTTPException(status_code=400, detail="Invalid ID")

    if result == "LIST_NOT_FOUND":
        raise HTTPException(status_code=404, detail="List not found")

    if result == "DUPLICATE":
        raise HTTPException(status_code=400, detail="Duplicate item")

    return {"message": "Item added"}


@router.put("/{list_id}")
def update_item(list_id: str, item: Item, service=Depends(get_service)):

    updated = service.update_item(list_id, item)

    if updated == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Updated"}


@router.patch("/{list_id}/{item_id}")
def patch_item(list_id: str, item_id: int, data: ItemPatch, service=Depends(get_service)):

    result = service.patch_item(list_id, item_id, data)

    if result == "INVALID_ID":
        raise HTTPException(status_code=400, detail="Invalid ID")

    if result == "NO_DATA":
        raise HTTPException(status_code=400, detail="No data")

    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Patched"}


@router.delete("/{list_id}/{item_id}")
def delete_item(list_id: str, item_id: int, service=Depends(get_service)):

    deleted = service.delete_item(list_id, item_id)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Deleted"}