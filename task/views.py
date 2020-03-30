# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Task, Subject, File
import datetime

class RemindersListView(ListView):
    template_name='task/reminders.html'
    model=Task

    def get_queryset(self):
        return Task.objects.filter(type_task='reminder')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        return context
    

class TasksListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        return Task.objects.filter(type_task='task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        return context

class TestsListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        return Task.objects.filter(type_task='test')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        

        return context

class SubjectsListView(ListView):
    template_name='task/subjects.html'
    model=Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        return context

class TaskDetailView(DetailView):
    template_name = 'task/task-view.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        obj = self.object
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        context["files"] = File.objects.filter(task=obj)
        return context    

class TestDetailView(DetailView):
    template_name = 'task/test-view.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = Task.objects.filter(time__range=[start_week, end_week])
        return context

