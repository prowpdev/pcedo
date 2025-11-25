from django.contrib import admin
from .models import MainFile, ChildFile

@admin.register(MainFile)
class MainFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number')

@admin.register(ChildFile)
class ChildFileAdmin(admin.ModelAdmin):
    list_display = ('file_type', 'main_file')
