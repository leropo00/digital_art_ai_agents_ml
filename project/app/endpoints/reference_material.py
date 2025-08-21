from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.database.session import get_db
from project.database.models.reference import ReferenceMaterial, ReferenceStorage
from project.database.schema.reference import (
    ReferenceMaterialCreate,
    ReferenceMaterialResponse,
    ReferenceStorageCreate,
    ReferenceStorageResponse,
)

router = APIRouter(
    prefix="/reference_material",
    tags=["Reference materials"],
    responses={HTTPStatus.NOT_FOUND: {"description": "Not found"}},
)


@router.post("/", response_model=ReferenceMaterialResponse)
async def create_reference_material(
    data: ReferenceMaterialCreate,
    db: AsyncSession = Depends(get_db),
):
    db_item = ReferenceMaterial(
        idea_type=data.idea_type,
        description=data.description,
    )
    if data.storage:
        for storage in data.storage:
            storage = ReferenceStorage(
                storage_type=storage.storage_type,
                storage_link=storage.storage_link,
            )
            db_item.storage.append(storage)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.post("/{reference_id}/storage", response_model=ReferenceStorageResponse)
async def create_reference_storage(
    reference_id: int,
    data: ReferenceStorageCreate,
    db: AsyncSession = Depends(get_db),
):
    result = (
        await db.execute(
            select(ReferenceMaterial).filter(ReferenceMaterial.id == reference_id)
        )
    ).scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Reference material not found"
        )

    db_item = ReferenceStorage(
        reference_material_id=reference_id,
        storage_type=data.storage_type,
        storage_link=data.storage_link,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
