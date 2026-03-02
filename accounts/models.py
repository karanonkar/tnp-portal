from django.db import models
from django.contrib.auth.models import AbstractUser


# ================= DEPARTMENT =================

class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ================= COMPANY =================

class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= JOB =================

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    package = models.CharField(max_length=100)
    eligibility_criteria = models.CharField(max_length=200)
    last_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"


# ================= CUSTOM USER =================

class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('tpo', 'TPO'),
        ('company', 'Company'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


# ================= APPLICATION =================

class Application(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'job')

    def __str__(self):
        return f"{self.student.username} applied for {self.job.title}"