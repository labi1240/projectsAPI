from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional, Union
from datetime import datetime
from bson import ObjectId
from slugify import slugify

IntOrFloat = Union[int, float]

class ImageModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    ImageName: Optional[str]
    ImageDescription: Optional[str]
    ImagePath: Optional[HttpUrl] = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda oid: str(oid)}

class UnitModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    br: Optional[IntOrFloat] = None  # Accept both int and float, convert float to int
    status: Optional[str] = None
    statusName: Optional[str] = None
    colType: Optional[str] = None
    unitType: Optional[str] = None
    unitName: Optional[str] = None
    ba: Optional[int] = None  # Bathrooms
    sqft: Optional[int] = None  # Square footage
    lotBalc: Optional[str] = None
    price: Optional[int] = None
    lastPrice: Optional[int] = None
    lastPriceWithValue: Optional[int] = None
    unitStyle: Optional[str] = None
    url: Optional[HttpUrl] = None
    image: Optional[HttpUrl] = None

    @validator('br', pre=True, always=True)
    def convert_br_to_int(cls, v):
        return int(v) if isinstance(v, float) else v

    @validator('url', 'image', pre=True, always=True)
    def validate_urls(cls, v):
        if v is not None and not v.startswith('http'):
            return f"https://{v}"
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda oid: str(oid)}

class ProjectModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    address: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None  # Made optional to handle None values
    bedrooms: Optional[str] = None
    buildingType: Optional[str] = None
    city_name: Optional[str] = None
    developer: Optional[str] = None
    developer_info: Optional[str] = None
    estimatedCompletion: Optional[str] = None
    images: List[ImageModel] = []
    incentives: Optional[str] = None
    price: Optional[str] = None
    province: Optional[str] = None
    sizeSqFt: Optional[str] = None
    status: Optional[str] = None
    street_name: Optional[str] = None
    summary: Optional[str] = None
    unitsStories: Optional[str] = None
    units: List[UnitModel] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    v: Optional[int] = Field(None, alias="__v")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat(),
        }