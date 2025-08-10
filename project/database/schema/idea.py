from pydantic import BaseModel
from typing import Optional
from project.database.models.idea import IdeaType

class ArtIdeaResponse(BaseModel):
    id: int
    identifier_name: str
    slug: str
    idea_type: IdeaType

    inital_idea: Optional[str]
    final_description: Optional[str]


class ArtIdeaCreate(BaseModel):
    identifier_name: str
    idea_type: IdeaType
    inital_idea: Optional[str]
    final_description: Optional[str]
