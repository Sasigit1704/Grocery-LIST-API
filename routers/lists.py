from fastapi import APIRouter, HTTPException
from schemas import GroceryList
from database import grocery_collection, metadata_collection

router = APIRouter(prefix="/list", tags=["List"])


@router.post("/")
def create_list(glist: GroceryList):

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

    lists = list(metadata_collection.find({}, {"_id": 0}))

    return lists


@router.get("/{list_id}")
def get_list(list_id: int):

    lst = grocery_collection.find_one({"listId": list_id}, {"_id": 0})

    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    return lst


@router.delete("/{list_id}")
def delete_list(list_id: int):

    grocery_collection.delete_one({"listId": list_id})
    metadata_collection.delete_one({"listId": list_id})

    return {"message": "List deleted successfully"}

@router.get("/filter/{name}")
def filter_lists(name: str):

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

    lists = list(
        metadata_collection.find({}, {"_id": 0})
        .sort("listName", 1)
    )

    return lists

@router.get("/group")
def group_items():

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