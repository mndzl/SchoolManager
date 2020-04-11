# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView
from django.http import JsonResponse
from .models import Task, Subject, File, Done
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .forms import CreateTaskForm, CreateSubjectForm

class RemindersListView(LoginRequiredMixin, ListView):
    template_name='task/reminders.html'
    model=Task

    def get_queryset(self):
        return Task.objects.filter(type_task='reminder', grade=self.request.user.student.grade)

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

        context['type_task'] = 'reminder'

        return context
    

class TasksListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        tasks = Task.objects.filter(type_task='task', grade=self.request.user.student.grade).order_by('time')
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
        every_task = Task.objects.filter(grade=self.request.user.student.grade, time__range=[start_week, end_week]).order_by('time')
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
        context['form_new_task'] = CreateTaskForm(grade=self.request.user.student.grade)

        return context

class TestsListView(ListView):
    template_name='task/tasks.html'
    model=Task
    def get_queryset(self):
        return Task.objects.filter(type_task='test', grade=self.request.user.student.grade ,time__gte=datetime.datetime.now()).order_by('time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        every_task = Task.objects.filter(grade=self.request.user.student.grade, time__range=[start_week, end_week]).order_by('time')

        context["week"] = []
        
        every_done = Done.objects.filter(user=self.request.user, grade=self.request.user.student.grade).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        context['task_dones'] = Task.objects.filter(grade=self.request.user.student.grade , type_task='test', time__lte=datetime.datetime.now()).order_by('time')
        context['q_dones'] = len(context['task_dones'])
        context['q_undones'] = len(self.get_queryset())     
        context['type_task'] = 'test'   
        context['form_new_task'] = CreateTaskForm(grade=self.request.user.student.grade)

        return context


class SubjectsListView(ListView):
    template_name='task/subjects.html'
    model=Subject
    
    def get_queryset(self):
        return Subject.objects.filter(grade=self.request.user.student.grade)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context["week"] = []
        every_task = Task.objects.filter(time__range=[start_week, end_week], grade=self.request.user.student.grade ).order_by('time')
        every_done = Done.objects.filter(user=self.request.user, grade=self.request.user.student.grade ).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)

        context['form_new_subject'] = CreateSubjectForm()
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
        every_task = Task.objects.filter(time__range=[start_week, end_week], grade=self.request.user.student.grade ).order_by('time')
        context["week"] = []
        every_done = Done.objects.filter(grade=self.request.user.student.grade ).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)
        context["files"] = File.objects.filter(task=obj, )
        context['is_done'] = len(Done.objects.filter(grade=self.request.user.student.grade, user=self.request.user, task=obj))

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
        every_task = Task.objects.filter(grade=self.requests.user.student.grade , time__range=[start_week, end_week]).order_by('time')
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

def newTask(request, typetask):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, grade=request.user.student.grade)
        if form.is_valid():
            form.save(commit=False)
            form.grade = request.user.student.grade
            form.save()
            task = Task.objects.latest('id')
            task.type_task = typetask
            task.save()
    
    return redirect(typetask+'s')


def newReminder(request):
    if request.method == 'POST':
        text = request.POST.get('description')
        Task.objects.create(type_task='reminder', description=text, grade=request.user.student.grade)

        return redirect('reminders')

def newSubject(request):
    print('enter')
    if request.method == 'POST':
        form = CreateSubjectForm(request.POST, request.FILES)
        print('Post handling')
        if form.is_valid():
            form.save(commit=False)
            form.grade = request.user.student.grade
            form.save()
    
    return redirect('subjects')

