from configs.genai import client
from google.genai import types
import re
import json
from fastapi import HTTPException

# -------------------File Understanding-------------------
class GenAIResponse:
    def upload_and_ask(self,file_bytes: bytes, file_name,question: str) -> str:

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
    
    def upload_resume(self,file_bytes: bytes, file_name) -> str:

        prompt = (
            f"📄 I have uploaded a resume file named {file_name}. "
            f"Please carefully read, analyze, and understand its content. \n\n"
            "Now provide a **detailed explanation and analysis** that a student/job seeker can easily understand. "
            "👉 Break down the answer step by step with clear points. "
            "📊 Highlight strengths, weaknesses, and areas of improvement. "
            "📝 Give actionable suggestions on how the resume can be improved (e.g., skills, formatting, keywords, achievements). "
            "📢 Use examples, analogies, and emojis to make the explanation engaging and memorable. "
            "Make sure the explanation is **long, structured, and insightful** so the student gains maximum value."
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

        return response._get_text(str)

    # -------------------Image Generation-------------------


    def generate_flowchart(self,concept: str) -> dict:
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
            model="gemini-2.5-flash",
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

    def generate_roadmap(self,student_prompt: str) -> str:
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
    

    

    
    def uploadimage_and_ask(self,image_bytes:bytes,image_name,question)-> str:

        prompt = (
            f"📘 You are a Student, and your Teacher has uploaded an image named **{image_name}**. "
            "Your task is to carefully observe and understand what’s shown in the image. 🧐\n\n"
            f"🎯 The Teacher asks: {question}\n\n"
            "💡 Explain your answer in a way that shows clear understanding:\n"
            "- Give a **simple and clear explanation** that anyone can understand. \n"
            "- Include **step-by-step reasoning** so it’s easy to follow. \n"
            "- Add **examples or comparisons** from real life to make it meaningful. 🌍\n"
            "- Use **emojis** to make your explanation fun and easy to remember. 😄\n\n"
            "🎓 Your goal is to **learn deeply**, show your thinking process clearly, "
            "and make sure your explanation proves that you truly understand the topic."
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            prompt
            ]
        )

        return response._get_text(str)
    

        # quize generation
    def generate_quize(self, analytics) -> str:
        prompt = f"""
        You are an intelligent tutor. Analyze this student's learning data
        and recommend one topic they should focus on next.
        Data: {analytics}

        Respond strictly in JSON format:
        {{
            "suggestion": "Motivational sentence for student.",
            "recommended_topic": "Topic name",
            "recommended_quiz_length": 10
        }}
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )

            
            return response.text

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini quiz generation failed{e}")