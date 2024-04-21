from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from users.forms import UserForm


# User Model Interactions
@login_required
@staff_member_required
def users(request):
    users = User.objects.all()

    if request.method == 'POST':
        person = request.POST['person']
        user = User.objects.get(pk=person)
        user.is_active = False
        user.save()
        messages.success(request, f"Deactivated Account for {user.first_name} {user.last_name}")
        redirect('users:users')

    return render(request, 'users/users.html', {'users': users})


def login_page(request):

    if request.user.is_authenticated:
        return redirect('partsdatabase:parts_db')

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('partsdatabase:parts_db')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')


def logout_action(request):
    logout(request)
    return redirect('login_page')


@login_required
@staff_member_required
def create_user(request):
    form = UserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('users:create_user')

    return render(request, 'users/create_user.html', {'form': form})

