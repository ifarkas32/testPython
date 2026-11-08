from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Egyszerű API")

# Egyszerű memóriabeli tároló (újraindításkor törlődik)
items: dict[int, dict] = {}
next_id = 1


class ItemIn(BaseModel):
    name: str
    price: float = 0.0


@app.get("/")
def root():
    return {"status": "ok", "message": "Az API működik"}


@app.get("/test", response_class=HTMLResponse, include_in_schema=False)
def test_page():
    return (Path(__file__).parent / "test_page.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/items")
def list_items():
    return list(items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Nem található")
    return items[item_id]


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    global next_id
    items[next_id] = {"id": next_id, **item.model_dump()}
    next_id += 1
    return items[next_id - 1]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Nem található")
    del items[item_id]
    return {"deleted": item_id}
