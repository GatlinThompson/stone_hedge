from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LogForm
from .models import Log
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@login_required
def logs(request):
    logs = Log.objects.all().order_by('-id')
    return render(request, 'partslog/partslog.html', {'logs': logs})


# Form to log user items
@login_required
def log_form(request):
    form = LogForm(request.POST or None)

    if request.method == 'POST':
        set_user = request.POST
        set_user._mutable = True
        set_user['name'] = set_user['name'].upper()
        set_user['created_by'] = request.user
        set_user._mutable = False

        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully logged {form.cleaned_data['name']}")
            return redirect('partslog:log_form')
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return render(request, 'partslog/log_form.html', {'form': form})


# Staff member views unapproved logs
@login_required
@staff_member_required
def approval(request):
    logs = Log.objects.filter(approved=False)
    return render(request, 'partslog/log_approval.html', {'logs': logs})


# Staff member approves a log
@login_required
@staff_member_required
def approve_item(request, item):
    log = Log.objects.get(pk=item)
    log.approved = True
    log.approved_by = User.objects.get(pk=request.user.id)
    log.save()
    return redirect('partslog:approval')
