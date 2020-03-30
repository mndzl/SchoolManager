"""schoolmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from task import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.RemindersListView.as_view(), name='reminders'),
    path('tasks/', views.TasksListView.as_view(), name='tasks'),
    path('tests/', views.TestsListView.as_view(), name='tests'),
    path('subjects/', views.SubjectsListView.as_view(), name='subjects'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='detail_task'),
    path('tests/<int:pk>', views.TestDetailView.as_view(), name='detail_test')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
