from django import forms
from .models import Subject, Task

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