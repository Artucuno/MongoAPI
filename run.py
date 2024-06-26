import os
from typing import Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import json_util

# Environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
WEB_IP = os.getenv("WEB_IP", "0.0.0.0")
WEB_PORT = os.getenv("WEB_PORT", 80)
AUTH_SECRET = os.getenv("AUTH_SECRET", None)
ARGS_ALLOWED = True if os.getenv("ARGS_ALLOWED", "0") == "1" else False


class MongoRequest(BaseModel):
    db: str = Field(..., title="Database name", description="The name of the database")
    collection: Optional[str] = Field(None, title="Collection name", description="The name of the collection")
    operation: str = Field(..., title="Operation", description="The operation to perform (pymongo method)")
    query: Optional[dict] = Field({}, title="Query", description="The query to perform")
    args: Optional[dict] = Field({}, title="Arguments", description="The arguments to pass to the operation")


class MongoAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.add_api_route("/", self.main_route, methods=["POST"])

    async def main_route(self, query: MongoRequest, request: Request):
        if AUTH_SECRET:  # If an auth secret is set, check if the request has the correct header
            if request.headers.get("Authorization") != AUTH_SECRET:
                return Response(status_code=403)
        db = self.client[query.db]
        if query.collection is None:
            result = await getattr(db, query.operation)(query.query, **query.args if ARGS_ALLOWED else {})
            return JSONResponse(content=result)
        collection = db[query.collection]
        func = getattr(collection, query.operation)
        try:
            result = await func(query.query, **query.args if ARGS_ALLOWED else {})
        except TypeError:
            result = []
            async for item in func(query.query, **query.args if ARGS_ALLOWED else {}):
                result.append(item)
        if isinstance(result, object):
            if hasattr(result, "__dict__"):
                result = vars(result)
            else:
                result = str(result)
        else:
            result = json_util.dumps(result)
        return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    app = MongoAPI()
    uvicorn.run(app, host=WEB_IP, port=int(WEB_PORT))
