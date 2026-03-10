from fastapi import APIRouter, HTTPException
from schemas import Item
from database import grocery_collection

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/{list_id}")
def get_items(list_id: int):
    """
    Retrieve all items from a specific grocery list.
    Args:
        list_id (int): ID of the grocery list.
    Returns:
        list: A list of items in the specified grocery list.
    Raises:
        HTTPException: If the grocery list is not found.
    """
    lst = grocery_collection.find_one({"listId": list_id}, {"_id": 0})

    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    return lst["items"]


@router.post("/{list_id}")
def add_item(list_id: int, item: Item):
    """
    Add a new item to a specific grocery list.
    Args:
        list_id (int): ID of the list where the item will be added.
        item (Item): Item details including id, name and quantity.
    Returns:
        dict: Confirmation message after adding the item.
    Raises:
        HTTPException: If the list does not exist or item ID already exists.
    """

    lst = grocery_collection.find_one({"listId": list_id})

    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    for i in lst["items"]:
        if i["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item ID already exists")

    grocery_collection.update_one(
        {"listId": list_id},
        {"$push": {"items": item.dict()}}
    )

    return {"message": "Item added successfully"}


@router.delete("/{list_id}/{item_id}")
def delete_item(list_id: int, item_id: int):
    """
    Delete an item from a grocery list.
    Args:
        list_id (int): ID of the grocery list.
        item_id (int): ID of the item to delete.
    Returns:
        dict: Confirmation message after deletion.
    Raises:
        HTTPException: If the item is not found.
    """

    result = grocery_collection.update_one(
        {"listId": list_id},
        {"$pull": {"items": {"id": item_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted"}