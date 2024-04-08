#main.py

from fastapi import FastAPI
from models import ProjectModel
import mongodb_utils
from fastapi import HTTPException
from typing import Optional
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await mongodb_utils.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await mongodb_utils.close_mongo_connection()

@app.get("/projects")
async def get_projects(
    incentives: Optional[str] = None,
    name: Optional[str] = None,
    price: Optional[str] = None,
    province: Optional[str] = None,
    sizeSqFt: Optional[str] = None,
    status: Optional[str] = None,
    street_name: Optional[str] = None,
):
    projects = await mongodb_utils.retrieve_projects(
        incentives=incentives,
        name=name,
        price=price,
        province=province,
        sizeSqFt=sizeSqFt,
        status=status,
        street_name=street_name,
    )
    return projects

@app.get("/projects/{project_name}", response_model=ProjectModel)
async def get_project(project_name: str):
    project_name = project_name.replace("-", " ")
    project = await mongodb_utils.retrieve_project(project_name)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")