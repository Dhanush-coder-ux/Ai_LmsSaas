from email.message import EmailMessage
from aiosmtplib import send
from jinja2 import Environment,FileSystemLoader
from configs.email import EMAIL_FROM,SMTP_HOST,SMTP_PORT,EMAIL_PASSWORD
from fastapi import HTTPException

env = Environment(loader=FileSystemLoader("templates"))

async def send_email(to_email: str, subject: str, template_name: str, context: dict):

    template = env.get_template(template_name)
    html_content = template.render(context)
    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content("This is a HTML email.")
    message.add_alternative(html_content, subtype="html")
    try:
        await send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=EMAIL_FROM,
            password=EMAIL_PASSWORD,
            start_tls=True,
        )
        raise HTTPException(status_code=200,detail='Email sended successfully !')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(f" Email sending failed: {e}")
