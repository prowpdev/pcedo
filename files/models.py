# files/models.py
from django.db import models

FILE_TYPE_CHOICES = (
    ('main', 'Main'),
    ('child', 'Child'),
)

class SpreadsheetFile(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    data = models.JSONField(default=dict)  # full table: {"columns": [], "rows": []}
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.file_type})"
