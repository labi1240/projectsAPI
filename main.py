from fastapi import FastAPI, HTTPException
from typing import List, Optional
import mongodb_utils
from models import ProjectModel
from slugify import slugify

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await mongodb_utils.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await mongodb_utils.close_mongo_connection()

@app.get("/projects", response_model=List[ProjectModel])
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
    # Dynamically add 'slug' to each project
    for project in projects:
        if 'name' in project and project['name']:
            project['slug'] = slugify(project['name'])
    return projects

@app.get("/projects/{project_name}", response_model=ProjectModel)
async def get_project(project_name: str):
    project = await mongodb_utils.retrieve_project(project_name.replace("-", " "))
    if project:
        project['slug'] = slugify(project['name']) if 'name' in project and project['name'] else 'unnamed-project'
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")
