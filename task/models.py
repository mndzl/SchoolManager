# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=70)
    color = models.CharField(max_length=7)
    teacher = models.CharField(max_length=50)
    schedule = models.FileField(null=True, blank=True, upload_to='media/')
    days = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    type_task = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.title + " ({})".format(self.type_task)

class File(models.Model):
    file_path = models.FileField(upload_to='media/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.file_path.name + " ({})".format(self.task.title) 

class Done(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task.title + " ({})".format(self.user.username)

