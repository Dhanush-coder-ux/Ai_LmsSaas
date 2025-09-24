from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = genai.Client(api_key=os.environ['GENAI_API_KEY'])


# -------------------File Understanding-------------------
def upload_and_ask(file_bytes: bytes, file_name,question: str) -> str:

    prompt = (
        f"📚 I have uploaded a student file name {file_name}. "
        f"Please read and understand its content thoroughly. \n\n"
        f"💡 Question: {question}\n\n"
        "Provide a **detailed explanation** in a way a student can understand easily. "
        "Use examples, analogies, and emojis to make it engaging. "
        "Make sure the explanation is **long, clear, and deep** so the student can get a full understanding."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=file_bytes,
                mime_type='application/pdf' 
            ),
            prompt
        ]
    )

    return response.text

# -------------------Image Generation-------------------


def generate_flowchart(concept: str) -> dict:
    prompt = (
        f"You are a professional diagram generator. "
        f"Generate a **Mermaid.js flowchart** and also give a clear explanation "
        f"for the following concept: {concept}. \n\n"
        "⚡ Rules: \n"
        "Use examples, analogies, and emojis to make it engaging. "
        "- Show Mermaid code inside a ```mermaid code block.\n"
        "- After the code block, write a step-by-step explanation of the flow.\n"
        "- Flow should be top-to-bottom (TD).\n"
        "- Use rectangles for steps, diamonds for decisions."
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt]
    )

    text = response.text
    mermaid_match = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
    mermaid_code = mermaid_match.group(1).strip() if mermaid_match else None
    explanation = re.sub(r"```mermaid\n.*?```", "", text, flags=re.DOTALL).strip()

    return {
        "diagram": mermaid_code,
        "explanation": explanation
    }


