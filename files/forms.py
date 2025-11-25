from django import forms
from .models import SpreadsheetFile

class SpreadsheetFileForm(forms.ModelForm):
    class Meta:
        model = SpreadsheetFile
        fields = ['name', 'file_type', 'parent']
