from dotenv import load_dotenv
import os
from openai import OpenAI
from ..models.external_models import gpt4o, o4_mini


def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model=o4_mini,
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
