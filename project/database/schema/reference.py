from typing import List, Optional

from pydantic import BaseModel

from project.database.models.reference import ReferenceMaterialType, StorageType


class ReferenceStorageCreate(BaseModel):
    storage_type: StorageType
    storage_link: str


class ReferenceStorageResponse(BaseModel):
    id: int
    storage_type: StorageType
    storage_link: str


class ReferenceMaterialCreate(BaseModel):
    reference_material_type: ReferenceMaterialType
    description: str
    storage: Optional[List[ReferenceStorageCreate]] = None


class ReferenceMaterialResponse(BaseModel):
    id: int
    reference_material_type: ReferenceMaterialType
    description: str
