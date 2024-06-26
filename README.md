# MongoAPI
A simple API to interact with Self-Hosted MongoDB Databases.

MongoAPI is built using FastAPI and Motor.

## About
This was built to allow me to interact with my MongoDB databases using Cloudflare Workers because of the lack of self-hosted MongoDB support.

## Usage
### Installation
```bash
git clone https://github.com/Artucuno/MongoAPI.git
cd MongoAPI
# Make sure to edit docker-compose.yml to your liking
docker-compose up -d
```

## API
The API is super simple and allows you to do most things that the MongoDB Driver allows you to do.

### Endpoints
There is only one endpoint, `/`, which is used to interact with the database.

> ### POST `/`
> Example Headers:
> ```json
> {
>     "Authorization": "secret"
> }
> ```
> Example body:
> ```json
> {
>     "db": "selected_db",
>     "collection": "my_collection",
>     "operation": "insert_one", // Any operation from the pymongo collection object
>     "query": {
>         "content": "Hello, World!"
>     }
> }
> ```
