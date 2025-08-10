from fastapi import APIRouter, Depends, HTTPException
import json
from http import HTTPStatus
from project.database.session import get_db
from project.database.models.idea import ArtIdea
from project.database.schema.idea import ArtIdeaResponse, ArtIdeaCreate

from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/art_ideas", tags=["Art Ideas"], 
    responses={HTTPStatus.NOT_FOUND: {"description": "Not found"}},
)

@router.get("/", response_model=List[ArtIdeaResponse])
def all_ideas(db: Session = Depends(get_db)):
    return db.query(ArtIdea).all()
    
@router.get("/{idea_id}", response_model=ArtIdeaResponse)
def get_idea(
        idea_id: int,
        db: Session = Depends(get_db),
    ):
    res = db.query(ArtIdea).filter(ArtIdea.id == idea_id).first()
    if not res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Idea not found")
    return res


@router.post("/")
def create_idea(
        data: ArtIdeaCreate,
        db: Session = Depends(get_db),
    ):
    print(data)
    
    db_item = ArtIdea(identifier_name=data.identifier_name,
                      idea_type= data.idea_type,
                      slug=data.identifier_name.lower(), 
                      inital_idea=data.inital_idea,
                      final_description=data.final_description,
                      )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item