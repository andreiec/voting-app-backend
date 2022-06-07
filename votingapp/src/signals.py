from django.db.models.signals import post_save

from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver

from django_rest_passwordreset.signals import reset_password_token_created

from src.models import User

import random
import string

def createUser(sender, instance, created, **kwargs):
    if created:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        instance.set_password(password)
        instance.save()

        subject = "Platformă de vot digital"
        message = f"Salut {instance.first_name}!\n\nBun venit pe platforma de votare, pentru a te autentifica folosește parola:\n{password}"
    
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )


@receiver(reset_password_token_created)
def passwordResetTokenCreated(sender, instance, reset_password_token, *args, **kwargs):
    subject = "Resetare parolă - Platformă vot"
    message = f"Salut,\nAi primit acest mail deoarece ai cerut resetarea parolei. Pentru a continua, accesează link-ul de mai jos\n\nhttp://localhost:3000/reset-password/?token={reset_password_token.key}\n\nÎn cazul în care nu ai cerut acest mail te rugăm sa contactezi administratorul."

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
        fail_silently=False
    )

post_save.connect(createUser, sender=User)
