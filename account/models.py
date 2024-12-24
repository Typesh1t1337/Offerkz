from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True,null=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    is_verified = models.BooleanField(default=False)

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id



