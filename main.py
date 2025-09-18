# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import uuid
from cosmos_client import get_container, ItemNotFoundError

app = FastAPI(title="FastAPI on Azure Functions + CosmosDB (NoSQL)")

class Item(BaseModel):
    id: Optional[str] = None
    pk: str                      # partition key (choose a field for partitioning)
    name: str
    description: Optional[str] = None

# dependency that returns a container instance (singletons in module-level are fine too)
def container_dep():
    return get_container()

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item, container=Depends(container_dep)):
    if not item.id:
        item.id = str(uuid.uuid4())
    doc = item.dict()
    # cosmos SDK expects the partition key property to exist in doc
    try:
        container.create_item(body=doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return doc

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str, pk: str, container=Depends(container_dep)):
    # We require partition key (pk) to read item efficiently
    try:
        item = container.read_item(item=item_id, partition_key=pk)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item not found: {e}")
    return item

@app.get("/items", response_model=List[Item])
def list_items(pk: Optional[str] = None, container=Depends(container_dep)):
    # simple query: list all or by partition key
    if pk:
        query = f"SELECT * FROM c WHERE c.pk = @pk"
        items = list(container.query_items(query=query, parameters=[{"name":"@pk","value":pk}], enable_cross_partition_query=True))
    else:
        items = list(container.read_all_items(max_item_count=100))
    return items

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item, container=Depends(container_dep)):
    # upsert will create or replace
    item.id = item_id
    try:
        res = container.upsert_item(body=item.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str, pk: str, container=Depends(container_dep)):
    try:
        container.delete_item(item=item_id, partition_key=pk)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {}
