from fastapi import APIRouter, HTTPException
from schemas import GroceryList
from database import grocery_collection, metadata_collection

router = APIRouter(prefix="/list", tags=["List"])

@router.post("/")
def create_list(glist: GroceryList):
    """
    Create a new grocery list.
    Args:
        glist (GroceryList): List information containing listId and listName.
    Returns:
        dict: Confirmation message after successful creation.
    Raises:
        HTTPException: If the list already exists.
    """
    existing = metadata_collection.find_one({"listId": glist.listId})

    if existing:
        raise HTTPException(status_code=400, detail="List already exists")

    grocery_collection.insert_one({
        "listId": glist.listId,
        "listName": glist.listName,
        "items": []
    })

    metadata_collection.insert_one({
        "listId": glist.listId,
        "listName": glist.listName
    })

    return {"message": "List created successfully"}


@router.get("/")
def get_all_lists():
    """
    Retrieve all existing grocery lists.
    Returns:
        list: A list containing listId and listName of all grocery lists.
    """
    lists = list(metadata_collection.find({}, {"_id": 0}))

    return lists


@router.get("/{list_id}")
def get_list(list_id: int):
    """
    Retrieve a specific grocery list along with its items.
    Args:
        list_id (int): ID of the grocery list.
    Returns:
        dict: Grocery list details including items.
    Raises:
        HTTPException: If the list is not found.
    """
    lst = grocery_collection.find_one({"listId": list_id}, {"_id": 0})

    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    return lst


@router.delete("/{list_id}")
def delete_list(list_id: int):
    """
    Delete a grocery list completely.
    Args:
        list_id (int): ID of the grocery list to delete.
    Returns:
        dict: Confirmation message after deletion.
    """
    grocery_collection.delete_one({"listId": list_id})
    metadata_collection.delete_one({"listId": list_id})

    return {"message": "List deleted successfully"}


@router.get("/filter/{name}")
def filter_lists(name: str):
    """
    Filter grocery lists by list name.
    Args:
        name (str): Name of the grocery list.
    Returns:
        list: Matching lists with the specified name.
    Raises:
        HTTPException: If no matching lists are found.
    """
    lists = list(
        metadata_collection.find(
            {"listName": name},
            {"_id": 0}
        )
    )

    if not lists:
        raise HTTPException(status_code=404, detail="No lists found")

    return lists


@router.get("/sort")
def sort_lists():
    """
    Retrieve all grocery lists sorted alphabetically by list name.
    Returns:
        list: Sorted list of grocery lists.
    """
    lists = list(
        metadata_collection.find({}, {"_id": 0})
        .sort("listName", 1)
    )

    return lists


@router.get("/group")
def group_items():
    """
    Group items across all grocery lists and calculate total quantity per item.
    Returns:
        list: Aggregated result showing item names and their total quantities.
    """
    pipeline = [
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": "$items.name",
                "total_quantity": {"$sum": "$items.quantity"}
            }
        }
    ]

    result = list(grocery_collection.aggregate(pipeline))

    return result