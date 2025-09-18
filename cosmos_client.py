# cosmos_client.py
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DB = os.environ.get("COSMOS_DATABASE", "fastapidb")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "items")

# lazy-initialize client/container singletons
_client = None
_database = None
_container = None

def _init():
    global _client, _database, _container
    if _client is None:
        if not COSMOS_ENDPOINT or not COSMOS_KEY:
            raise Exception("COSMOS_ENDPOINT and COSMOS_KEY must be set in environment")
        _client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        # create db/container if not exists (safe in dev, in prod you may want infra-as-code)
        _database = _client.create_database_if_not_exists(id=COSMOS_DB)
        _container = _database.create_container_if_not_exists(
            id=COSMOS_CONTAINER,
            partition_key=PartitionKey(path="/pk"),   # we are using "pk" as partition key
            offer_throughput=400
        )

def get_container():
    _init()
    return _container

class ItemNotFoundError(Exception):
    pass
