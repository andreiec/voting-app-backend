from django.db.models.signals import post_save

from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver

from django_rest_passwordreset.signals import reset_password_token_created

from src.models import User

import random
import string
import threading


# Class for email threding
class EmailThread(threading.Thread):
    def __init__(self, subject, content, from_address, recipient_list):
        self.subject = subject
        self.content = content
        self.from_address = from_address
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run (self):
        send_mail(
            self.subject,
            self.content,
            self.from_address,
            self.recipient_list,
            fail_silently=False
        )

def createUser(sender, instance, created, **kwargs):
    if created:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        instance.set_password(password)
        instance.save()

        subject = "Platformă de vot digital"
        message = f"Salut {instance.first_name}!\n\nBun venit pe platforma de votare, pentru a te autentifica folosește parola:\n{password}"

        EmailThread(subject, message, settings.EMAIL_HOST_USER, [instance.email]).start()


@receiver(reset_password_token_created)
def passwordResetTokenCreated(sender, instance, reset_password_token, *args, **kwargs):
    subject = "Resetare parolă - Platformă vot"
    message = f"Salut,\nAi primit acest mail deoarece ai cerut resetarea parolei. Pentru a continua, accesează link-ul de mai jos\n\nhttp://localhost:3000/reset-password/?token={reset_password_token.key}\n\nÎn cazul în care nu ai cerut acest mail te rugăm sa contactezi administratorul."

    EmailThread(subject, message, settings.EMAIL_HOST_USER, [instance.email]).start()

post_save.connect(createUser, sender=User)
