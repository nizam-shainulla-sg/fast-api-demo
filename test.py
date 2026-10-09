from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/")
def read_root():
    return {"message": "Hello from test"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.post("/items")
def create_item(item: dict):
    return {"created": item}


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": item_id}
