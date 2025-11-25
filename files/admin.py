from django.contrib import admin
from .models import SpreadsheetFile
from django import forms
import json

class SpreadsheetFileForm(forms.ModelForm):
    # Pretty JSON display in admin
    data = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':80}), required=False)

    class Meta:
        model = SpreadsheetFile
        fields = '__all__'

    def clean_data(self):
        data = self.cleaned_data['data']
        if data:
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format.")
            return json_data
        return {}

class SpreadsheetFileAdmin(admin.ModelAdmin):
    form = SpreadsheetFileForm
    list_display = ('name', 'file_type', 'created_at', 'updated_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(SpreadsheetFile, SpreadsheetFileAdmin)
