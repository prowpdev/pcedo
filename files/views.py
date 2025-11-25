# files/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import SpreadsheetFile
from .forms import SpreadsheetFileForm
import json

def file_list(request):
    files = SpreadsheetFile.objects.all()
    return render(request, 'files/file_list.html', {'files': files})

def file_edit(request, pk=None):
    if pk:
        file = get_object_or_404(SpreadsheetFile, pk=pk)
    else:
        file = None

    if request.method == "POST":
        form = SpreadsheetFileForm(request.POST, instance=file)
        if form.is_valid():
            saved_file = form.save(commit=False)
            # Save initial empty data if new
            if not saved_file.data:
                saved_file.data = {"columns": ["ID", "Name"], "rows": []}
            saved_file.save()
            return redirect('file_edit', pk=saved_file.pk)
    else:
        form = SpreadsheetFileForm(instance=file)

    # Pass data to template
    data_json = json.dumps(file.data if file else {"columns": ["ID", "Name"], "rows": []})

    return render(request, 'files/file_edit.html', {
        'form': form,
        'file': file,
        'data_json': data_json
    })

def save_file_data(request, pk):
    if request.method == "POST":
        file = get_object_or_404(SpreadsheetFile, pk=pk)
        table_data = json.loads(request.POST.get('tableData', '{}'))
        file.data = table_data
        file.save()
        return JsonResponse({'status': 'success'})
