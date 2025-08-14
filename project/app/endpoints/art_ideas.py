from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.database.models.idea import ArtIdea
from project.database.schema.idea import ArtIdeaCreate, ArtIdeaResponse
from project.database.session import get_db

router = APIRouter(
    prefix="/art_ideas",
    tags=["Art Ideas"],
    responses={HTTPStatus.NOT_FOUND: {"description": "Not found"}},
)


@router.get("/", response_model=List[ArtIdeaResponse])
async def all_ideas(db: AsyncSession = Depends(get_db)):
    return await db.scalars(select(ArtIdea))


@router.get("/{idea_id}", response_model=ArtIdeaResponse)
async def get_idea(
    idea_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = (
        await db.execute(select(ArtIdea).filter(ArtIdea.id == idea_id))
    ).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Idea not found")
    return result


@router.post("/")
async def create_idea(
    data: ArtIdeaCreate,
    db: AsyncSession = Depends(get_db),
):
    db_item = ArtIdea(
        identifier_name=data.identifier_name,
        idea_type=data.idea_type,
        slug=data.identifier_name.lower(),
        inital_idea=data.inital_idea,
        final_description=data.final_description,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
