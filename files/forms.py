from django import forms
from .models import SpreadsheetFile

class SpreadsheetFileForm(forms.ModelForm):
    class Meta:
        model = SpreadsheetFile
        fields = ['name', 'file_type', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'p-2'
            }),
            'file_type': forms.TextInput(attrs={
                'class': 'p-2'
            }),
            'parent': forms.Select(attrs={
                'class': 'p-2'
            }),
        }
