from django.db import models

# Main File (Parent)
class MainFile(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100, unique=True)
    data = models.JSONField(default=dict)  # dynamic columns like Cash on Hand, Petty Cash

    def __str__(self):
        return f"{self.name} ({self.account_number})"

# Child File
class ChildFile(models.Model):
    main_file = models.ForeignKey(MainFile, on_delete=models.CASCADE, related_name='child_files')
    file_type = models.CharField(max_length=255)  # e.g., "Cash Recipient Journal"
    data = models.JSONField(default=dict)  # dynamic columns like OR Number, Debit, Credit

    def __str__(self):
        return f"{self.file_type} for {self.main_file.account_number}"
