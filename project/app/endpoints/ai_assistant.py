import os
from typing import AsyncGenerator

from fastapi import APIRouter, status, WebSocket
from openai import AsyncOpenAI

from project.database.schema.ai_assistant import AiSuggestTitle

from project.database.session import get_db

router = APIRouter(
    prefix="/ai_assistant",
    tags=["AI Assistant"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.websocket("/echo")
async def websocket_endpoint(websocket: WebSocket):
    """
    Echo endpoint to test how websockets work
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"ECHO, send back data: {data}")


async def get_ai_response(message: str) -> AsyncGenerator[str, None]:
    """
    OpenAI Response
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant, skilled in explaining "
                    "complex concepts in simple terms."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        stream=True,
    )

    all_content = ""
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            all_content += content
            yield all_content



@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response(message):
            await websocket.send_text(text)


@router.post("/suggest_title")
async def suggest_title_for_idea(
    # data: AiSuggestTitle,
):

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
