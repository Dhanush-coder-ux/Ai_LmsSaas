from configs.genai import client
from google.genai import types
import re

# -------------------File Understanding-------------------
class GenAIResponse:
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
    
    #-------------------Roadmap Generation-------------------

    def generate_roadmap(student_prompt: str) -> str:
        prompt = (
            f"You are an expert AI Learning Path Designer. "
            f"Your task is to create a **personalized, step-by-step learning roadmap** "
            f"based on the student’s request: {student_prompt}. \n\n"
            "⚡ Rules for Roadmap:\n"
            "1. Break the roadmap into **phases** (Beginner → Intermediate → Advanced).\n"
            "2. Use **time-based milestones** (e.g., Week 1–2, Month 1, Month 3).\n"
            "3. Each milestone must include **topics, skills, tools, and a small project**.\n"
            "4. Suggest **resources** (docs, courses, books, or platforms).\n"
            "5. Make it **practical and industry-ready**.\n\n"
            "📊 Evaluation:\n"
            "1. **Compare** this roadmap with at least **2 standard AI-generated roadmaps** (assume they exist).\n"
            "2. Highlight **strengths** of this roadmap.\n"
            "3. Highlight **weaknesses or gaps** compared to others.\n"
            "4. Suggest **improvements** to make it the best possible roadmap.\n\n"
            "✅ Output Format:\n"
            "1. **Personalized Roadmap** (with phases + timeline)\n"
            "2. **Comparison with Other AI Roadmaps**\n"
            "3. **Evaluation & Suggested Improvements**"
        )

        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt
        ]
        )
        

        return response._get_text(str)
