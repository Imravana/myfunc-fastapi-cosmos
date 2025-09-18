# myfunc-fastapi-cosmos
Azure Function App with Python (FastAPI) + Cosmos DB (NoSQL) providing RESTful CRUD APIs. Runs locally and on Azure Functions using AsgiMiddleware to serve FastAPI via HTTP triggers. Cosmos DB with partition key ensures efficient queries and scalable data handling.

# Azure Function + FastAPI + Cosmos DB (NoSQL)

Azure Function App with Python (FastAPI) + Cosmos DB (NoSQL) providing RESTful CRUD APIs.  
Runs locally and on Azure Functions using **AsgiMiddleware** to serve FastAPI via HTTP triggers.  
Cosmos DB with partition key ensures efficient queries and scalable data handling.

---

## Features
- ✅ FastAPI integrated with Azure Functions (ASGI middleware)
- ✅ CRUD (Create, Read, Update, Delete) APIs
- ✅ Azure Cosmos DB (NoSQL) backend
- ✅ Runs locally with `func start` or deployed to Azure
- ✅ Partition key support for efficient queries

---

## Prerequisites
- [Python 3.12](https://www.python.org/downloads/release/python-3120/)  
- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local)  
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)  
- [Visual Studio Code](https://code.visualstudio.com/) (recommended)  

---

## Local Setup

1. **Clone the repo**
   
   ->git clone https://github.com/Imravana/myfunc-fastapi-cosmos.git

   ->cd myfunc-fastapi-cosmos

3. **Create a virtual environment**

->python -m venv .venv
->.venv\Scripts\activate   # (Windows)
->source .venv/bin/activate  # (Linux/Mac)

3. **Install dependencies**

->pip install -r requirements.txt

4. **Cosmos db NoSQL cred**

-> Update the cosmos db creds in the local.settings.json

4. **Run the function locally**

->func start
