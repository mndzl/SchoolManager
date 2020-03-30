# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

admin.site.register(models.Subject)
admin.site.register(models.Task)
admin.site.register(models.File)
admin.site.register(models.Done)
# Register your models here.
