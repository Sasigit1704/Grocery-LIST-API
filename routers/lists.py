from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from schemas import GroceryList
from services.database import get_db
from services.list_service import ListService

router = APIRouter(prefix="/list", tags=["List"])


def get_service(db=Depends(get_db)):
    return ListService(db)


@router.post("/")
def create_list(glist: GroceryList, service=Depends(get_service)):

    result = service.create_list(glist)

    if not result:
        raise HTTPException(status_code=400, detail="List already exists")

    return {"message": "Created", "list_id": result}


@router.get("/")
def get_lists(
    name: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
    group: bool = False,
    service=Depends(get_service)
):

    result = service.get_lists(name, sort_order, group)

    if not result:
        raise HTTPException(status_code=404, detail="No data found")

    return result


@router.get("/{list_id}")
def get_list(list_id: str, service=Depends(get_service)):

    lst = service.get_list_by_id(list_id)

    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    return lst


@router.delete("/{list_id}")
def delete_list(list_id: str, service=Depends(get_service)):

    deleted = service.delete_list(list_id)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="List not found")

    return {"message": "Deleted"}