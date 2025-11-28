from django import forms
from .models import SpreadsheetFile

class SpreadsheetFileForm(forms.ModelForm):
    class Meta:
        model = SpreadsheetFile
        fields = ['name', 'file_type', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'p-2 mt-1 block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 '
            }),
            'file_type': forms.Select(attrs={
                'class': 'p-2 mt-1 block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150'
            }),
            'parent': forms.Select(attrs={
                'class': 'p-2 mt-1 block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150'
            }),
        }
