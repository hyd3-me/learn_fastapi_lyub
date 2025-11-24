from fastapi import APIRouter, HTTPException, status
from model.explorer import Explorer
import data.explorer as service

# import fake.explorer as service
from typing import Union, Optional

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer:
    print(name)
    result = service.get_one(name)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Explorer '{name}' not found"
        )
    return result


# все остальные конечные точки пока ничего не делают:
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("/")
def modify(explorer: Explorer) -> Explorer:
    return service.modify(explorer)


@router.put("/")
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)
