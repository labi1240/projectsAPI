from typing import Optional

from pydantic import BaseModel, Field


class ImageModel(BaseModel):
    ImageName: Optional[str] = None
    ImageDescription: str
    ImagePath: str

class ProjectModel(BaseModel):
    _id: str
    address: str
    slug: Optional[str]
    bedrooms: str
    buildingType: str
    city_name: str
    developer: str
    developer_info: str
    estimatedCompletion: str
    images: list[ImageModel]
