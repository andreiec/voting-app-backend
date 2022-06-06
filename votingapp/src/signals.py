from django.db.models.signals import post_save

from django.core.mail import send_mail
from django.conf import settings

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
            [instance.email, 'andreiec112@gmail.com'],
            fail_silently=False,
        )

post_save.connect(createUser, sender=User)