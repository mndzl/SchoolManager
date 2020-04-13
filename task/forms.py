from django import forms
from .models import Subject, Task, File

class CreateTaskForm(forms.ModelForm):
    title = forms.CharField(label='Título')
    time = forms.DateField(label='Fecha de entrega', widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea, label='Descripción')
    subject = forms.ModelChoiceField(label='Elige la materia', queryset=Subject.objects.all())

    class Meta:
        model = Task
        fields = ['subject', 'title', 'description', 'time']

    def __init__(self, *args, **kwargs):
        grade = kwargs.pop('grade', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(grade=grade)

class CreateSubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=70, label='Nombre')
    teacher = forms.CharField(max_length=50, label='Profesor')
    schedule = forms.FileField(required=False, label='Programa')
    days = forms.CharField(max_length=100, label='Dias de clase', empty_value='Dias por confirmar')

    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'days', 'schedule']

class FileFieldForm(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = File
        fields = ['file_path']
        