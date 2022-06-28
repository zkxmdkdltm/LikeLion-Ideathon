from statistics import mode
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('C', '선택안함'),
    ]
    trinity_id = models.CharField(max_length=128)
    nickname = models.CharField(max_length=10)
    address = models.CharField(max_length=128)
    confirm = models.CharField(max_length=128)    
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=255)
    email = models.TextField(blank=True, max_length=255)
    email_verify = models.TextField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
