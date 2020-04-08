from django.db import models
from django.contrib.auth.models import User

class Grade(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #grade = models.ForeignKey(Grade, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username + f' ({self.grade.name})'
