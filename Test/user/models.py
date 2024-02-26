from django.contrib.auth.models import AbstractUser
from django.db import models


class UserSet(models.Model):
    GENDER_CHOICE = (("UNKNOWN", "unknown"),
                     ("MALE", "male"),
                     ("FEMALE", "female"))
    uid = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(blank=True, null=True)
    height = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="UNKNOWN")  # 0:boy, 1:girl
    fcm_id = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.name)


# Create your models here.
class UserProfile(AbstractUser):
    uid = models.CharField(max_length=100, blank=True)
    database = models.OneToOneField(UserSet, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return str(self.get_username())
