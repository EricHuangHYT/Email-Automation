import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail

load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.getenv("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"))

message = Mail(
    from_email=os.getenv("FROM_EMAIL"),
    to_emails="erichyt873@gmail.com",
    subject="Test email",
    plain_text_content="This is a test."
)

try:
    response = sg.client.mail.send.post(request_body=message.get())
    print(f"Status: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Body: {e.body}")