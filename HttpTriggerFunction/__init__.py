import os
import azure.functions as func
from fastapi import FastAPI, Request, HTTPException, Query
from azure.cosmos import CosmosClient, PartitionKey
from azure.functions import AsgiMiddleware

app = FastAPI()

# Cosmos DB connection
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
COSMOS_DB = os.environ["COSMOS_DATABASE"]
COSMOS_CONTAINER = os.environ["COSMOS_CONTAINER"]

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = client.create_database_if_not_exists(id=COSMOS_DB)
container = db.create_container_if_not_exists(
    id=COSMOS_CONTAINER,
    partition_key=PartitionKey(path="/pk"),
    offer_throughput=400
)

# ---------------- POST /items ----------------
@app.post("/items")
async def create_item(request: Request):
    data = await request.json()
    if "id" not in data:
        raise HTTPException(status_code=400, detail="Missing 'id' field")
    if "pk" not in data:
        raise HTTPException(status_code=400, detail="Missing 'pk' (partition key) field")
    item = container.create_item(data)
    return {"message": "Item created in Cosmos DB", "item": item}

# ---------------- GET /items/{item_id} ----------------
@app.get("/items/{item_id}")
async def read_item(item_id: str, pk: str = Query(..., description="Partition key")):
    try:
        item = container.read_item(item=item_id, partition_key=pk)
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------- PUT /items/{item_id} ----------------
@app.put("/items/{item_id}")
async def update_item(item_id: str, pk: str = Query(..., description="Partition key"), request: Request = None):
    body = await request.json()
    try:
        item = container.read_item(item=item_id, partition_key=pk)
        for k, v in body.items():
            item[k] = v
        container.upsert_item(item)
        return {"message": "Item updated", "item": item}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------- DELETE /items/{item_id} ----------------
@app.delete("/items/{item_id}")
async def delete_item(item_id: str, pk: str = Query(..., description="Partition key")):
    try:
        container.delete_item(item=item_id, partition_key=pk)
        return {"message": "Item deleted", "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------- Optional: GET /items (list all) ----------------
@app.get("/items")
async def list_items(pk: str = Query(..., description="Partition key")):
    query = f"SELECT * FROM c WHERE c.pk=@pk"
    items = list(container.query_items(
        query=query,
        parameters=[{"name": "@pk", "value": pk}],
        enable_cross_partition_query=True
    ))
    return {"items": items}

# ---------------- Azure Functions entry point ----------------
async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await AsgiMiddleware(app).handle_async(req, context)
