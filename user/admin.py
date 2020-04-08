from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'grade')
    list_filter = ('grade',)

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = 'Nombre'

admin.site.register(Student, StudentAdmin)