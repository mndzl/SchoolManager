# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Subject,
    Task,
    File,
    Done,
    Grade
)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'teacher')
    list_filter = ('grade', 'teacher')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade')
    list_filter = ('grade', 'subject')

class FileAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'task', 'grade')
    list_filter = ('grade', 'task')

class DoneAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'time', 'grade')
    list_filter = ('grade', 'user', 'task')

class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'password')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Done, DoneAdmin)
admin.site.register(Grade, GradeAdmin)
# Register your models here.
