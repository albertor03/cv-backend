from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class SendEmail(object):

    @staticmethod
    def send_simple_message(to: str, subject: str, body: str):
        error = str()
        try:
            message = EmailMultiAlternatives(subject,  body, settings.EMAIL_HOST_USER, [to])
            message.send()
        except Exception as e:
            error = str(e)

        return error
