#mongodb_utils.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS, DB_NAME, COLLECTION_NAME
from typing import Optional
client: AsyncIOMotorClient = None

def get_database():
    return client[DB_NAME]

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DETAILS)

async def close_mongo_connection():
    client.close()

async def retrieve_projects():
    collection = get_database()[COLLECTION_NAME]
    projects = []
    async for project in collection.find():
        projects.append(project)
    return projects

async def retrieve_project(name: str):
    collection = get_database()[COLLECTION_NAME]
    # Use a case-insensitive search
    project = await collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    if project:
        project['slug'] = project['name'].replace(' ', '-')
    return project

async def retrieve_projects(
    incentives: Optional[str] = None,
    name: Optional[str] = None,
    price: Optional[str] = None,
    province: Optional[str] = None,
    sizeSqFt: Optional[str] = None,
    status: Optional[str] = None,
    street_name: Optional[str] = None,
):
    collection = get_database()[COLLECTION_NAME]
    filter_params = {
        k: v
        for k, v in {
            "incentives": incentives,
            "name": name,
            "price": price,
            "province": province,
            "sizeSqFt": sizeSqFt,
            "status": status,
            "street_name": street_name,
        }.items()
        if v is not None
    }
    projects = []
    async for project in collection.find(filter_params):
        project['slug'] = project['name'].replace(' ', '-')
        projects.append(project)
    return projects