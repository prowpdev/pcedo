from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import AdminLoginForm

def admin_custom_login(request):
    error_message = None  # <-- NEW

    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user and user.is_staff:
                login(request, user)
                return redirect('/admin/')
            else:
                error_message = "Invalid username or password"  # <-- NEW
    else:
        form = AdminLoginForm()

    return render(request, 'accounts/admin_login.html', {
        "form": form,
        "error_message": error_message   # <-- NEW
    })
