from configs.genai import client
from google.genai  import types

class TeacherGainAIResponse:
    
    def upload_and_ask(self,file_bytes: bytes, file_name,question: str) -> str:

        teacher_prompt = (
            f"📘 A Teacher has uploaded a file named **{file_name}**. "
            "Your task is to carefully read, analyze, and deeply understand the content of this file. \n\n"
            f"❓ The Teacher asks: {question}\n\n"
            "📝 Provide a **comprehensive explanation** that is:\n"
            "- Clear, step-by-step, and easy to follow. \n"
            "- Rich with **examples, analogies, and real-life applications**. \n"
            "- Uses **emojis** to make learning engaging and memorable. \n"
            "- Written in a way that a Teacher can confidently explain to students. \n\n"
            "⚡ Make sure your explanation is **detailed, deep, and well-structured**, "
            "so the Teacher can gain full mastery of the topic and pass it on effectively."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type='application/pdf' 
                ),
                teacher_prompt
            ]
        )

        return response._get_text(str)
    
    def uploadimage_and_ask(self,image_bytes:bytes,image_name,question)-> str:

        prompt =(
               f"📘 A Teacher has uploaded a image named **{image_name}**. "
            "Your task is to carefully read, analyze, and deeply understand the content of this image. \n\n"
            f"❓ The Teacher asks: {question}\n\n"
            "📝 Provide a **comprehensive explanation** that is:\n"
            "- Clear, step-by-step, and easy to follow. \n"
            "- Rich with **examples, analogies, and real-life applications**. \n"
            "- Uses **emojis** to make learning engaging and memorable. \n"
            "- Written in a way that a Teacher can confidently explain to students. \n\n"
            "⚡ Make sure your explanation is **detailed, deep, and well-structured**, "
            "so the Teacher can gain full mastery of the topic and pass it on effectively."
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