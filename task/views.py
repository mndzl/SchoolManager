# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.shortcuts import render

def reminders(request):
    return render(request, 'task/reminders.html')