import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_answer(question: str, sources: list[dict]) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to the .env file.")

    context = ""

    for number, source in enumerate(sources, start=1):
        context += (
            f"\nSource [{number}] — {source['file_name']}\n"
            f"{source['snippet']}\n"
        )

    prompt = f"""
You are Guidely, an internal company knowledge assistant.

Answer only using the provided sources.
Write a short and clear answer.
If the sources do not contain the answer, say that clearly.
At the end of each factual sentence, cite its source number, for example [1].
Do not invent information.

Question:
{question}

Provided sources:
{context}
"""

    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    if not interaction.output_text:
        raise RuntimeError("Gemini returned an empty answer.")

    return interaction.output_text