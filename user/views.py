from django.shortcuts import render
from .models import Student, Grade
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import StudentRegisterForm

def register(request):
    if (request.method == 'POST'):
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            Student.objects.create(user=user, grade=grade)
            login(request, user)
            return redirect('reminders')
    else:
        form = StudentRegisterForm()

    return render(request, 'user/register.html', {'form':form})

