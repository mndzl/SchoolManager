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
from task import views as views_task
from user import views as views_user
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views_task.RemindersListView.as_view(), name='reminders'),
    path('tasks/', views_task.TasksListView.as_view(), name='tasks'),
    path('tests/', views_task.TestsListView.as_view(), name='tests'),
    path('subjects/', views_task.SubjectsListView.as_view(), name='subjects'),
    path('tasks/<int:pk>', views_task.TaskDetailView.as_view(), name='detail_task'),
    path('tests/<int:pk>', views_task.TestDetailView.as_view(), name='detail_test'),
    path('tasks/<int:pk>/done', views_task.toggleTask, name='done-task'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views_user.register, name='register'),
    path('new_task/<str:type_task>', views_task.newTask, name='new_task'),
    path('tasks/<int:pk>/delete', views_task.TaskDeleteView.as_view(), name='delete_task'),
    path('tests/<int:pk>/delete', views_task.TaskDeleteView.as_view(), name='delete_test'),
    path('reminders/<int:pk>/delete', views_task.TaskDeleteView.as_view(), name='delete_reminder'),
    path('subjects/<int:pk>/delete', views_task.SubjectDeleteView.as_view(), name='delete_subject'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
