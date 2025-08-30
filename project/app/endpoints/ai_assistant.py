import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from project.database.schema.ai_assistant import AiSuggestTitle

from project.database.session import get_db

router = APIRouter(
    prefix="/ai_assistant",
    tags=["AI Assistant"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/suggest_title")
async def suggest_title_for_idea(
    # data: AiSuggestTitle,
):
    # async and sync client use same methods
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = await client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "system",
                "content": """You create memorable titles of artistic ideas, up to five words,
                            base on described ideas, take into accout mood in xml tags if present.
                            Output mutlitple ideas if possible, each inside xml tag <idea>.""",
            },
            {
                "role": "user",
                "content": """Octopus is squished inside a human skull in such a way, 
                    that its tentacles appear at bottom and its eyes can be seen through eyelids. <mood>scary</mood>""",
            },
        ],
    )

    print(completion.choices)

    return completion.choices


""""

## completion.choices

[
  {
    "finish_reason": "stop",
    "index": 0,
    "logprobs": null,
    "message": {
      "content": "<idea>Skullbound Cephalopod Terror</idea>\n<idea>Eyes Through Squirming Eyelids</idea>\n<idea>Abyssal Tentacles in Skull</idea>\n<idea>Cranial Octopus of Dread</idea>\n<idea>Skeletal Grasp from Within</idea>",
      "refusal": null,
      "role": "assistant",
      "annotations": [],
      "audio": null,
      "function_call": null,
      "tool_calls": null
    }
  }
]
"""
