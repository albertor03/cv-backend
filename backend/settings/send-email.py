import requests
import os


class SendEmail:

    def __init__(self):
        self.baseUrl = os.environ['MAILGUN_BASE_URL']
        self.mailgunVersion = os.environ['MAILGUN_VERSION']
        self.mailgunDomain = os.environ['MAILGUN_DOMAIN']
        self.apiKey = os.environ['MAILGUN_API_KEY']
        self.fromEmail = os.environ['MAILGUN_FROM_EMAIL']

    def send_simple_message(self, to: str, subject: str, body: str):
        return requests.post(
            f"{self.baseUrl}/{self.mailgunVersion}/{self.mailgunDomain}/message",
            auth=("api", self.apiKey),
            data={"from": self.fromEmail,
                  "to": [to, to],
                  "subject": subject,
                  "text": body})
