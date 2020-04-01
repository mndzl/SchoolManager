from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(error_messages={'unique': 'Este correo ya está asociado a una cuenta.'})
    username = forms.CharField(label='DNI', error_messages={'unique': 'Ya te has registrado anteriormente.'})
    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(max_length=50, label='Apellido')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name','password1','password2']