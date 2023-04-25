
from .models import Task
from django import forms

#Creamos formularios en base a los modelos creados.

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a Title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description'}),
            'priority': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }

# Estilizar los forms desde forms.py


