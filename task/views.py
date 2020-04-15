# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.http import JsonResponse
from .models import Task, Subject, File, Done, Grade
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from .forms import CreateTaskForm, CreateSubjectForm, FileFieldForm, PutInGradeForm
from django.urls import resolve
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms


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
        every_task = Task.objects.filter(grade=self.request.user.student.grade, time__range=[start_week, end_week]).order_by('time')

        every_done = Done.objects.filter(user=self.request.user).values('task')
        every_done_ids = []
        for i in range(len(every_done)):
            every_done_ids.append(every_done[i]["task"])

        for task in every_task.iterator():
            if task.id not in every_done_ids:
                context["week"].append(task)

        context['type_task'] = 'reminder'
        context['form_select_grade'] = PutInGradeForm()

        return context

    def post(self, request, *args, **kwargs):
        text = request.POST.get('description')
        Task.objects.create(type_task='reminder', description=text, grade=request.user.student.grade)

        return redirect('reminders')
    

class TasksListView(LoginRequiredMixin, ListView):
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
        context['new_file_form'] = FileFieldForm()

        return context

class TestsListView(LoginRequiredMixin, ListView):
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
        context['new_file_form'] = FileFieldForm()
        return context


class SubjectsListView(LoginRequiredMixin, ListView):
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



class TaskDetailView(LoginRequiredMixin, DetailView):
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
        context["files"] = File.objects.filter(task=obj)
        context['is_done'] = len(Done.objects.filter(grade=self.request.user.student.grade, user=self.request.user, task=obj))
        context['update_form'] = CreateTaskForm(instance=self.get_object(), grade=self.request.user.student.grade)
        context['new_file_form'] = FileFieldForm()
        context['files'] = File.objects.filter(task=self.get_object())

        return context   

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = CreateTaskForm(instance=instance, data=request.POST, grade=request.user.student.grade)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_by = request.user
            task.save()

        if len(request.FILES) > 0:
            old_files = File.objects.filter(task=self.get_object())
            for file_model in old_files:
                file_model.delete()

            for file_model in request.FILES.getlist('file_field'):
                File.objects.create(task=self.get_object(), file_path=file_model)

        return redirect('tasks')

class TestDetailView(LoginRequiredMixin, DetailView):
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

class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    success_message = 'La actividad se ha borrado.'

    def test_func(self):
        return self.request.user.student.delegate

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TaskDeleteView, self).delete(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        url_splitted = current_url.split('_')
        type_task = url_splitted[1]
        self.success_url = reverse(f'{type_task}s')
        return self.post(request, *args, **kwargs)

class SubjectDeleteView(UserPassesTestMixin ,DeleteView):
    model = Subject
    success_message = 'La materia se ha borrado.'
    success_url = '/subjects/'

    def test_func(self):
        return self.request.user.student.delegate

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

        
@login_required
def toggleTask(request, pk):

    if request.user.student.grade is None:
        return redirect('reminders')

    if request.method == 'GET':
        task = Task.objects.get(id=pk)
        if (Done.objects.filter(task=task, user=request.user).count()):
            Done.objects.get(task=task, user=request.user).delete()
        else:
            Done.objects.create(task=task, user=request.user, time=datetime.datetime.now())

        return JsonResponse({'result':'done'}, status=200)

    return JsonResponse({'error':""}, status=400)

@login_required
def newTask(request, type_task):

    if request.user.student.grade is None:
        return redirect('reminders')

    if request.method == 'POST':
        form = CreateTaskForm(request.POST, grade=request.user.student.grade)
        if form.is_valid():
            task = form.save(commit=False)
            task.grade = request.user.student.grade
            task.type_task = type_task
            task.save()

        for file_model in request.FILES.getlist('file_field'):
            File.objects.create(file_path=file_model, task=task, grade=request.user.student.grade)
    
    return redirect(type_task+'s')

@login_required
def putInGrade(request):

    if request.method == 'POST':
        form = PutInGradeForm(request.POST)
        if form.is_valid():
            grade_id = request.POST.get('grade')
            grade = Grade.objects.get(id=grade_id)
            password_user = request.POST.get('password')
            if grade.password == password_user:
                student = request.user.student
                student.grade = grade
                student.save()
                return redirect('reminders')
            
            form.add_error('password', 'La contraseña no es válida')
            return render(request, 'task/reminders.html',{'form_select_grade':form})



