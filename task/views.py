# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

def reminders(request):
    return render(request, 'task/reminders.html')

def tasks(request):
    return render(request, 'task/tasks.html')