from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class SendEmail(object):

    def __init__(self):
        self.emailFromUser = settings.EMAIL_HOST_USER
        self.emailReply = settings.EMAIL_REPLY

    def send_simple_message(self, to: str, subject: str, body: str):
        error = str()
        try:
            message = EmailMultiAlternatives(subject,  body, self.emailFromUser, [to],
                                             reply_to=[self.emailReply])
            message.send()
        except Exception as e:
            error = str(e)

        return error
