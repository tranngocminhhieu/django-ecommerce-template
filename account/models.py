from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='account/avatar', blank=True, null=True)

class Address(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.pk}'
