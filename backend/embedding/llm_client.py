import json
import os

from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


load_dotenv()


class LLMClient:
    """
    Gemini client for grounded BIS recommendations.

    A single instance is reused across API requests.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt,
        )

        output = interaction.output_text

        if not output:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return output.strip()

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any],
        response_model: type[BaseModel],
    ) -> BaseModel:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if not schema:
            raise ValueError(
                "Schema cannot be empty."
            )

        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": schema,
            },
        )

        output = interaction.output_text

        if not output:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            data = json.loads(output)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise RuntimeError(
                "Gemini JSON response must be an object."
            )

        try:
            validated_response = response_model.model_validate(
                data
            )

        except Exception as exc:
            raise RuntimeError(
                "Gemini response failed Pydantic validation."
            ) from exc

        return validated_response


@lru_cache(maxsize=1)
def get_llm_client() -> LLMClient:
    """
    Return the single shared Gemini client.

    The client is created only once per API process.
    """

    return LLMClient()