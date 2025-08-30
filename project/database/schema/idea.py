from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from project.database.models.idea import IdeaType, TitleType


class ArtIdeaResponse(BaseModel):
    id: int
    identifier_name: str
    slug: str
    idea_type: IdeaType
    initial_idea: Optional[str]
    final_description: Optional[str]


class ArtIdeaCreate(BaseModel):
    identifier_name: str
    idea_type: IdeaType
    initial_idea: Optional[str]
    final_description: Optional[str]


class ArtIdeaUpdate(BaseModel):
    initial_idea: str
    final_description: str


class ArtIdeaTitleResponse(BaseModel):
    id: int
    title_text: str
    title_type: TitleType


class ArtIdeaTitleCreate(BaseModel):
    title_text: str
    title_type: TitleType


class ArtIdeaTitleUpdate(BaseModel):
    title_text: str


class ArtIdeaQuestionResponse(BaseModel):
    id: int
    question_text: str
    solved_date: Optional[datetime]


class ArtIdeaQuestionCreate(BaseModel):
    question_text: str


class ArtQuestionTextUpdate(BaseModel):
    question_text: str


class ArtIdeaResponseDetails(ArtIdeaResponse):
    titles: Optional[List[ArtIdeaTitleResponse]] = None
    questions: Optional[List[ArtIdeaQuestionResponse]] = None
