from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from project.database.models.idea import ArtIdea, ArtIdeaTitle, ArtIdeaQuestion
from project.database.schema.idea import (
    ArtIdeaCreate,
    ArtIdeaTitleUpdate,
    ArtIdeaTitleCreate,
    ArtIdeaQuestionCreate,
    ArtIdeaResponse,
    ArtIdeaTitleResponse,
    ArtIdeaQuestionResponse,
)
from project.database.session import get_db

router = APIRouter(
    prefix="/art_ideas",
    tags=["Art Ideas"],
    responses={HTTPStatus.NOT_FOUND: {"description": "Not found"}},
)


@router.get("/", response_model=List[ArtIdeaResponse])
async def all_ideas(db: AsyncSession = Depends(get_db)):
    return await db.scalars(select(ArtIdea))


@router.get("/{idea_id}")
async def get_idea(
    idea_id: int,
    include_titles: bool = False,
    include_questions: bool = False,
    db: AsyncSession = Depends(get_db),
):
    query = select(ArtIdea).filter(ArtIdea.id == idea_id)
    options: List[ExecutableOption] = []
    if include_questions:
        options.append(selectinload(ArtIdea.questions))

    if include_titles:
        options.append(selectinload(ArtIdea.titles))

    if options:
        query = query.options(*options)

    result = (await db.execute(query)).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Idea not found")

    # TODO for now return without pydantic serialization
    # it seems that pydantic trigger lazy loading of unloaded relationships
    # this triggers the following error: https://docs.sqlalchemy.org/en/14/errors.html#error-xd2s
    return result


@router.post("/", response_model=ArtIdeaResponse, status_code=status.HTTP_201_CREATED)
async def create_idea(
    data: ArtIdeaCreate,
    db: AsyncSession = Depends(get_db),
):
    db_item = ArtIdea(
        identifier_name=data.identifier_name,
        idea_type=data.idea_type,
        # TODO create a slug function
        slug=data.identifier_name.lower(),
        initial_idea=data.initial_idea,
        final_description=data.final_description,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.post(
    "/{art_idea_id}/title",
    response_model=ArtIdeaTitleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_idea_title(
    art_idea_id: int,
    data: ArtIdeaTitleCreate,
    db: AsyncSession = Depends(get_db),
):
    result = (
        await db.execute(select(ArtIdea).filter(ArtIdea.id == art_idea_id))
    ).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Idea not found")

    db_item = ArtIdeaTitle(
        art_idea_id=art_idea_id,
        title_text=data.title_text,
        title_type=data.title_type,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.put(
    "/{art_idea_id}/title/{title_id}",
    response_model=ArtIdeaTitleResponse,
)
async def update_idea_title(
    art_idea_id: int,
    title_id: int,
    data: ArtIdeaTitleUpdate,
    db: AsyncSession = Depends(get_db),
):
    title = (
        await db.execute(select(ArtIdeaTitle).filter(ArtIdeaTitle.id == title_id))
    ).scalar_one_or_none()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")

    title.title_text = data.title_text
    title.title_type = data.title_type
    await db.commit()
    await db.refresh(title)
    return title


@router.post(
    "/{art_idea_id}/question",
    response_model=ArtIdeaQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_idea_questions(
    art_idea_id: int,
    data: ArtIdeaQuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    result = (
        await db.execute(select(ArtIdea).filter(ArtIdea.id == art_idea_id))
    ).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Idea not found")

    db_item = ArtIdeaQuestion(
        art_idea_id=art_idea_id,
        question_text=data.question_text,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
