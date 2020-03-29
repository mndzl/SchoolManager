# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=70)
    color = models.CharField(max_length=7)
    teacher = models.CharField(max_length=50)
    schedule = models.FileField()

class Task(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateField()
    description = models.CharField(max_length=1000)
    type_task = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class File(models.Model):
    file_path = models.FileField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Done(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)