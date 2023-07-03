from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='users_images')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    


class EmailVerif(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self) -> str:
        return f'EmailVerification object for {self.user.email}'
    
    def send_virification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подверждение учетной записи для {self.user.username}'
        message = 'Для подверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email = "from@example.com",
            recipient_list = [self.user.email],
            fail_silently=False,
        )
    def is_expired(self):
        return True if now() >= self.expiration else False