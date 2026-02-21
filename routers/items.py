from fastapi import APIRouter, HTTPException
from schemas import Item, ItemUpdate, ItemPatch
import json

router = APIRouter(prefix="/items", tags=["Items"])

FILE_PATH = "grocery.json"

def read_data():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def write_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


# GET all items
@router.get("/")
def get_items():
    data = read_data()
    return data["items"]


# POST add new item
@router.post("/")
def create_item(item: Item):
    data = read_data()
    items = data["items"]
    # check duplicate id
    for existing in items:
        if existing["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item ID already exists")
    new_item = {
        "id": item.id,
        "name": item.name,
        "quantity": item.quantity
    }
    items.append(new_item)
    write_data(data)
    return new_item

# PUT full update
@router.put("/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
    data = read_data()
    items = data["items"]
    for i in range(len(items)):
        if items[i]["id"] == item_id:
            items[i]["name"] = item.name
            items[i]["quantity"] = item.quantity
            write_data(data)
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")

# PATCH partial update
@router.patch("/{item_id}")
def patch_item(item_id: int, item: ItemPatch):
    data = read_data()
    items = data["items"]
    for i in range(len(items)):
        if items[i]["id"] == item_id:
            if item.name is not None:
                items[i]["name"] = item.name
            if item.quantity is not None:
                items[i]["quantity"] = item.quantity
            write_data(data)
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE item
@router.delete("/{item_id}")
def delete_item(item_id: int):
    data = read_data()
    items = data["items"]
    for i in range(len(items)):
        if items[i]["id"] == item_id:
            deleted_item = items[i]
            del items[i]
            write_data(data)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")