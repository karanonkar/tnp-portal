from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('tpo', 'TPO'),
        ('company', 'Company'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)