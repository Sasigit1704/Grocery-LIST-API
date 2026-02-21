from fastapi import APIRouter, HTTPException
import json

router = APIRouter(prefix="/list", tags=["List"])

FILE_PATH = "grocery.json"

def read_data():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def write_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# DELETE entire list
@router.delete("/")
def delete_list():
    data = read_data()
    if not data["items"]:
        raise HTTPException(status_code=404, detail="List is already empty")
    data["items"] = []
    write_data(data)
    return {"message": "Entire list deleted successfully"}

# GET total quantity
@router.get("/quantity")
def get_total_quantity():
    data = read_data()
    items = data["items"]
    total_quantity = sum(item["quantity"] for item in items)
    return {"total_quantity": total_quantity}