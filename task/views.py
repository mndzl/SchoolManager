# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from .models import Task, Subject, File, Done
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

class RemindersListView(LoginRequiredMixin, ListView):
    template_name='task/reminders.html'
    model=Task

    def get_queryset(self):
        return Task.objects.filter(type_task='reminder')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = []
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')

        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        return context
    

class TasksListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        tasks = Task.objects.filter(type_task='task').order_by('time')
        tasks_undone = []
        for task in tasks:
            if (len(Done.objects.filter(task=task, user=self.request.user))==0):
                tasks_undone.append(task)

        return tasks_undone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday()-1)
        end_week = start_week + datetime.timedelta(7)
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')
        context["week"] = []
        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)

        context['task_dones'] = Done.objects.filter(user=self.request.user)
        context['q_dones'] = len(context['task_dones'])
        context['q_undones'] = len(self.get_queryset())
        context['type_task'] = 'task'

        return context

class TestsListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        return Task.objects.filter(type_task='test', time__gte=datetime.datetime.now()).order_by('time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')

        context["week"] = []
        
        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        context['task_dones'] = Task.objects.filter(type_task='test', time__lte=datetime.datetime.now()).order_by('time')
        context['q_dones'] = len(context['task_dones'])
        context['q_undones'] = len(self.get_queryset())     
        context['type_task'] = 'test'   

        return context

class SubjectsListView(ListView):
    template_name='task/subjects.html'
    model=Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = []
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')
        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
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
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')
        context["week"] = []
        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        context["files"] = File.objects.filter(task=obj)
        context['is_done'] = len(Done.objects.filter(user=self.request.user, task=obj))

        return context    

class TestDetailView(DetailView):
    template_name = 'task/test-view.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = []
        every_task = Task.objects.filter(time__range=[start_week, end_week]).order_by('time')
        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        return context
        
def toggleTask(request, pk):
    if request.method == 'GET':
        task = Task.objects.get(id=pk)
        if (Done.objects.filter(task=task, user=request.user).count()):
            Done.objects.get(task=task, user=request.user).delete()
        else:
            Done.objects.create(task=task, user=request.user, time=datetime.datetime.now())

        return JsonResponse({'result':'done'}, status=200)

    return JsonResponse({'error':""}, status=400)



