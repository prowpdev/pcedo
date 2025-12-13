from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import SpreadsheetFile
from .forms import SpreadsheetFileForm
import json
from collections import defaultdict
from django.db.models import F

def home(request):
    return render(request, 'index.html')

def file_lists(request):
    """
    Retrieves only the top-level (root) files to display a hierarchical structure.
    Children will be accessed via the 'children' related_name in the template.
    """
    
    # Fetch all files that have NO parent (i.e., they are root/top-level entries)
    # Order them alphabetically.
    root_files = SpreadsheetFile.objects.filter(parent__isnull=True).order_by('name')

    # Note: We can simplify the context since we are just passing the root list
    context = {
        'files': root_files,  # Renamed for simplicity in the template loop
    }

    # 4. Render the template
    return render(request, 'files/type/lists.html', context)

def file_create(request, parent_id=None, file_id=None):
    """
    Creates a new spreadsheet file or updates an existing one.
    - If file_id is provided → update existing file
    - If parent_id is provided → create child file
    """

    # Determine if editing existing file or creating new
    file_instance = None
    if file_id:
        file_instance = SpreadsheetFile.objects.filter(pk=file_id).first()

    if request.method == "POST":
        form = SpreadsheetFileForm(request.POST, instance=file_instance)

        if form.is_valid():
            saved_file = form.save(commit=False)
    
            # Detect if NEW file (no primary key yet)
            is_new_file = saved_file.pk is None

            # Assign parent for NEW CHILD files
            if is_new_file:
                if saved_file.parent:
                    parent_id = saved_file.parent.pk
                if parent_id:
                    parent_file = SpreadsheetFile.objects.filter(pk=parent_id).first()
                    if parent_file:
                        saved_file.parent = parent_file
                        saved_file.file_type = "child"
                    else:
                        saved_file.file_type = "main"
                else:
                    saved_file.file_type = "main"

                # Ensure JSON structure exists
                if not saved_file.data:
                    saved_file.data = {"columns": [], "rows": []}

            saved_file.save()

            return redirect('file_edit', pk=saved_file.pk)

    else:
        form = SpreadsheetFileForm(instance=file_instance)

    return render(request, 'files/type/create_file.html', {
        'form': form,
        'parent_id': parent_id,
        'file_instance': file_instance,
    })



def file_list(request):
    """List all spreadsheet files"""
    files = SpreadsheetFile.objects.all()
    return render(request, 'files/file_list.html', {'files': files})


def file_edit(request, pk=None, parent_id=None):
    """
    Create or edit a spreadsheet file.
    If creating a new child file, pass parent_id to link it to main file.
    """
    if pk:
        file = get_object_or_404(SpreadsheetFile, pk=pk)
    else:
        file = None

    if request.method == "POST":
        form = SpreadsheetFileForm(request.POST, instance=file)
        if form.is_valid():
            saved_file = form.save(commit=False)

            # Assign parent if this is a new child file
            if not saved_file.pk:  # new file
                if parent_id:
                    try:
                        parent_file = SpreadsheetFile.objects.get(pk=parent_id)
                        saved_file.parent = parent_file
                        saved_file.file_type = 'child'
                    except SpreadsheetFile.DoesNotExist:
                        saved_file.file_type = 'main'
                else:
                    saved_file.file_type = 'main'

            # Initialize data if empty
            if not saved_file.data:
                saved_file.data = {"columns": [], "rows": []}

            saved_file.save()
            return redirect('file_edit', pk=saved_file.pk)
    else:
        form = SpreadsheetFileForm(instance=file)

    # Determine mainfile_id for template
    mainfile_id = None
    if file:
        file_type = (file.file_type or "").strip().lower()
        if file_type == 'child' and file.parent:
            mainfile_id = file.parent.pk
        else:
            mainfile_id = file.pk
    elif parent_id:
        mainfile_id = parent_id  # new child with parent
    
    # Pass parent columns if child
    parent_columns = []
    parent_column_values = {}
    if file and file.file_type.lower() == 'child' and file.parent:
        parent_data = file.parent.data
        for col_obj in parent_data.get("columns", []):
            col_name = col_obj if isinstance(col_obj, str) else col_obj.get("name")
            if col_name:
                parent_columns.append(col_name)
                # Collect unique values for dropdown
                parent_column_values[col_name] = list({row.get(col_name, "") for row in parent_data.get("rows", [])})

    # Pass data to template
    data_json = json.dumps(file.data if file else {"columns": [], "rows": []})

    if file:
        if (file.file_type or "").lower() == "child" and file.parent:
            parent_rows = []
            if file and file.file_type.lower() == "child" and file.parent:
                parent_rows = file.parent.data.get("rows", [])
            # ensure parent_column_values entries are lists of strings (unique)
            for k, v in parent_column_values.items():
                parent_column_values[k] = [str(x) if x is not None else "" for x in sorted(set(v))]

            data_json = json.dumps(file.data if file else {"columns": [], "rows": []})
            return render(request, 'files/type/child_file_edit.html', {
                'form': form,
                'file': file,
                'data_json': data_json,
                'mainfileId': mainfile_id,
                'parent_columns': parent_columns,
                'parent_column_values': parent_column_values,
                'parent_rows': parent_rows,
                'parent_file_data':file.parent
            })
        else:
            return render(request, 'files/type/main_file_edit.html', {
                'form': form,
                'file': file,
                'data_json': data_json,
                'mainfileId': mainfile_id,
                'parent_columns': parent_columns,
                'parent_column_values': parent_column_values,
            })

def save_file_data(request, pk):
    """Save spreadsheet data (columns + rows) via AJAX"""
    if request.method == "POST":
        file = get_object_or_404(SpreadsheetFile, pk=pk)
        table_data = request.POST.get('tableData', '{}')
        try:
            table_data_json = json.loads(table_data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        file.data = table_data_json
        file.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)
