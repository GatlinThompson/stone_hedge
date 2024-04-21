from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (Kit, Hardware, KitHardwareAssembly, Part, HardwareKit, HardwareKitAssembly,
                     PartHKAssembly, KitHardwareKit, KitPartAssembly)
from .forms import (KitForm, KitHardwareAssemblyForm, HardwareForm, PartForm,
                    HardwareKitForm, HardwareKitAssemblyForm, PartHKAssemblyForm, KitHKAssemblyForm, KitPartAssemblyForm)
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@login_required
def parts_db(request):
    # Loops array to create block for user's direction
    overview = [
        {
            'title': 'Hardware',
            'bg_color': '#9ED096',
            'links': [
                {
                    'href': 'partsdatabase:create_hardware',
                    'perms': request.user.has_perm('partsdatabase.add_hardware'),
                    'text': 'Create Hardware',
                },
                {
                    'href': 'partsdatabase:hardware',
                    'text': 'View Hardware',
                },
            ]
        },
        {
            'title': 'Hardware Kits',
            'bg_color': '#AA88D6',
            'links': [
                {
                    'href': 'partsdatabase:create_harwarekit',
                    'perms': request.user.has_perm('partsdatabase.add_hardwarekit'),
                    'text': 'Create Hardware Kit',
                },
                {
                    'href': 'partsdatabase:hardwarekit',
                    'text': 'View Hardware Kits',
                },
            ]
        },
        {
            'title': 'Parts',
            'bg_color': '#A7AB73',
            'links': [
                {
                    'href': 'partsdatabase:create_part',
                    'perms': request.user.has_perm('partsdatabase.add_part'),
                    'text': 'Create Part',
                },
                {
                    'href': 'partsdatabase:part',
                    'text': 'View Parts',
                },
            ]
        },
        {
            'title': 'Kits',
            'bg_color': '#3D6385',
            'links': [
                {
                    'href': 'partsdatabase:create_kit',
                    'perms': request.user.has_perm('partsdatabase.add_kit'),
                    'text': 'Create Kit',
                },
                {
                    'href': 'partsdatabase:kit',
                    'text': 'View Kits',
                },
            ]
        },
        {
            'title': 'Log',
            'bg_color': '#BB832F',
            'links': [
                {
                    'href': 'partslog:approval',
                    'perms': request.user.has_perm('partsdatabase.add_hardware'),
                    'text': 'Approve Logs',
                },
                {
                    'href': 'partslog:log_form',
                    'text': 'Log Item',
                },
                {
                    'href': 'partslog:logs',
                    'text': 'View Logs',
                },
            ]
        },
        {
            'perms': request.user.is_staff,
            'title': 'Users',
            'bg_color': '#A7495A',
            'links': [
                {
                    'href': 'users:create_user',
                    'perms': request.user.is_staff,
                    'text': 'Create User',
                },
                {
                    'href': 'users:users',
                    'perms': request.user.is_staff,
                    'text': 'Manage Users',
                },
            ]
        },
    ]

    return render(request, 'partsdatabase/overview/parts_db.html', {'overview': overview})


"""
Kit CRUD
"""

@login_required
def kit(request):
    kits = Kit.objects.all()
    return render(request, 'partsdatabase/kit/kit.html', {'kits': kits})


@login_required
@staff_member_required
def create_kit(request):
    form = KitForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            kit = form.save(commit=False)
            kit.name = kit.name.upper()
            kit.save()
            messages.success(request, f"{kit.name} Created Successfully")
            return redirect('partsdatabase:details_kit', kit.id)
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return render(request, 'partsdatabase/kit/kit_create_form.html', {'form': form})


@login_required
@staff_member_required
def delete_kit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    kit.delete()
    messages.success(request, f"{kit.name} Successfully Deleted")
    return redirect('partsdatabase:kit')


@login_required
@staff_member_required
def update_kit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    form = KitForm(request.POST or None, instance=kit)

    if request.method == 'POST':
        set_kit = request.POST
        set_kit._mutable = True
        set_kit['name'] = set_kit['name'].upper()
        set_kit._mutable = False

        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data['name']} Successfully Updated")
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
def details_kit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    kit_form = KitForm(request.POST or None, instance=kit)
    kit_hk_form = KitHKAssemblyForm(request.POST or None, kit=kit.id)
    kit_hw_form = KitHardwareAssemblyForm(request.POST or None, kit=kit.id)
    kit_part_form = KitPartAssemblyForm(request.POST or None, kit=kit.id)
    context = {
        'kit': kit,
        'kit_form': kit_form,
        'kit_hk_form': kit_hk_form,
        'kit_hw_form': kit_hw_form,
        'kit_part_form': kit_part_form
    }

    return render(request, 'partsdatabase/kit/details_kit.html', context)


"""
Kit HK CRUD
"""


@login_required
@staff_member_required
def kit_hk_form_submit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    form = KitHKAssemblyForm(request.POST or None)

    if request.method == 'POST':
        set_kit = request.POST
        set_kit._mutable = True
        set_kit['kit'] = kit
        set_kit._mutable = False

        if form.is_valid():
            form.save()

        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_hk_edit(request, kit_id, hk_id):
    kit_hk = KitHardwareKit.objects.get(pk=hk_id, kit=kit_id)

    if request.method == 'POST':
        qty = request.POST.get(f"hk_qty_{hk_id}", '')

        if int(qty) > 0:
            kit_hk.quantity = int(qty)
            kit_hk.save()
            messages.success(request, f"Successfully Updated {kit_hk.hardware_kit.name}")
        else:
            messages.success(request, f"Successfully Removed {kit_hk.hardware_kit.name}")
            kit_hk.delete()

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_hk_delete(request, kit_id, hk_id):
    kit_hk = KitHardwareKit.objects.get(pk=hk_id, kit=kit_id)
    kit_hk.delete()
    messages.success(request, f"Successfully Removed {kit_hk.hardware_kit.name}")
    return redirect('partsdatabase:details_kit', kit_id)


"""
Kit Hardware CRUD
"""


@login_required
@staff_member_required
def kit_hw_form_submit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    form = KitHardwareAssemblyForm(request.POST or None)

    if request.method == 'POST':
        set_kit = request.POST
        set_kit._mutable = True
        set_kit['kit'] = kit
        set_kit._mutable = False

        if form.is_valid():
            form.save()

        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_hw_edit(request, kit_id, hw_id):
    kit_hw = KitHardwareAssembly.objects.get(pk=hw_id, kit=kit_id)

    if request.method == 'POST':
        qty = request.POST.get(f"hardware_qty_{hw_id}", '')

        if int(qty) > 0:
            kit_hw.quantity = int(qty)
            kit_hw.save()
            messages.success(request, f"Successfully Updated {kit_hw.hardware.name}")
        else:
            messages.success(request, f"Successfully Removed {kit_hw.hardware.name}")
            kit_hw.delete()

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_hw_delete(request, kit_id, hw_id):
    kit_hw = KitHardwareAssembly.objects.get(pk=hw_id, kit=kit_id)
    kit_hw.delete()
    messages.success(request, f"Successfully Removed {kit_hw.hardware.name}")
    return redirect('partsdatabase:details_kit', kit_id)


"""
Kit Part CRUD
"""


@login_required
@staff_member_required
def kit_part_form_submit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    form = KitPartAssemblyForm(request.POST or None)

    if request.method == 'POST':
        set_kit = request.POST
        set_kit._mutable = True
        set_kit['kit'] = kit
        set_kit._mutable = False

        if form.is_valid():
            form.save()

        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_part_edit(request, kit_id, part_id):
    kit_part = KitPartAssembly.objects.get(pk=part_id, kit=kit_id)

    if request.method == 'POST':
        qty = request.POST.get(f"part_qty_{part_id}", '')

        if int(qty) > 0:
            kit_part.quantity = int(qty)
            kit_part.save()
            messages.success(request, f"Successfully Updated {kit_part.part.name}")
        else:
            messages.success(request, f"Successfully Removed {kit_part.part.name}")
            kit_part.delete()

    return redirect('partsdatabase:details_kit', kit_id)


@login_required
@staff_member_required
def kit_part_delete(request, kit_id, part_id):
    kit_part = KitPartAssembly.objects.get(pk=part_id, kit=kit_id)
    kit_part.delete()
    messages.success(request, f"Successfully Removed {kit_part.part.name}")
    return redirect('partsdatabase:details_kit', kit_id)


"""
Hardware CRUD
"""


@login_required
def hardware(request):
    hardwares = Hardware.objects.all()
    return render(request, 'partsdatabase/hardware/hardware.html', {'hardwares': hardwares})


@login_required
@staff_member_required
def create_hardware(request):
    form = HardwareForm(request.POST or None)
    last_hardware = Hardware.objects.last()

    if request.method == 'POST':
        if form.is_valid():
            hardware_form = form.save(commit=False)
            hardware_form.name = hardware_form.name.upper()
            form.save()
            messages.success(request, f"{hardware_form.name} Created Successfully")
            return redirect('partsdatabase:hardware')
        else:
            for field, error in form.errors.items():
                messages.error(request,f"{error}")

    context = {
        'form': form,
        'last_hardware': last_hardware,
        'crud': 'Create'
    }

    return render(request, 'partsdatabase/hardware/hardware_form.html', context)


@login_required
@staff_member_required
def update_hardware(request, hardware_id):
    hardware = Hardware.objects.get(pk=hardware_id)
    form = HardwareForm(request.POST or None, instance=hardware)

    if request.method == 'POST':
        if form.is_valid():
            hardware_form = form.save(commit=False)
            hardware_form.name = hardware_form.name.upper()
            form.save()
            messages.success(request, f"{hardware_form.name} Updated Successfully")
            return redirect('partsdatabase:hardware')
        else:
            for field, error in form.errors.items():
                messages.error(request,f"{error}")

    context = {
        'form': form,
        'hardware': hardware,
        'crud': 'Update'
    }

    return render(request, 'partsdatabase/hardware/hardware_form.html', context)


@login_required
@staff_member_required
def delete_hardware(request, hardware_id):
    hardware = Hardware.objects.get(pk=hardware_id)
    hardware.delete()
    messages.error(request, f"{hardware.name} Successfully Deleted")
    return redirect('partsdatabase:hardware')


"""
Part CRUD
"""


@login_required
def part(request):
    parts = Part.objects.all()
    return render(request, 'partsdatabase/part/part.html', {'parts': parts})


@login_required
@staff_member_required
def create_part(request):
    form = PartForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            part_form = form.save(commit=False)
            part_form.name = part_form.name.upper()
            form.save()
            messages.success(request, f"{part_form.name} Created Successfully")
            return redirect('partsdatabase:part')
        else:
            for field, error in form.errors.items():
                messages.error(request,f"{error}")

    context = {
        'form': form,
        'crud': 'Create'
    }

    return render(request, 'partsdatabase/part/part_form.html', context)


@login_required
@staff_member_required
def update_part(request, part_id):
    part = Part.objects.get(pk=part_id)
    form = PartForm(request.POST or None, instance=part)

    if request.method == 'POST':
        if form.is_valid():
            part_form = form.save(commit=False)
            part_form.name = part_form.name.upper()
            form.save()
            messages.success(request, f"{part_form.name} Updated Successfully")
            return redirect('partsdatabase:part')
        else:
            for field, error in form.errors.items():
                messages.error(request,f"{error}")

    context = {
        'form': form,
        'hardware': hardware,
        'crud': 'Update'
    }

    return render(request, 'partsdatabase/part/part_form.html', context)


@login_required
@staff_member_required
def delete_part(request, part_id):
    part = Part.objects.get(pk=part_id)
    part.delete()
    messages.error(request, f"{part.name} Successfully Deleted")
    return redirect('partsdatabase:part')


"""
Hardware Kit CRUD
"""


@login_required
def hardwarekit(request):
    hardware_kits = HardwareKit.objects.all()
    return render(request, 'partsdatabase/hardwarekit/hardwarekit.html', {'hardware_kits': hardware_kits})


@login_required
@staff_member_required
def create_hardwarekit(request):
    form = HardwareKitForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            hardwarekit = form.save(commit=False)
            hardwarekit.name = hardwarekit.name.upper()
            hardwarekit.save()

            return redirect('partsdatabase:details_hardwarekit', hardwarekit.id)
        else:
            for field, error in form.errors.items():
                messages.error(request,f"{error}")

    return render(request, 'partsdatabase/hardwarekit/hardwarekit_form.html', {'form': form})


@login_required
def details_hardwarekit(request, hardwarekit_id):
    hardwarekit = HardwareKit.objects.get(pk=hardwarekit_id)
    hardware_form = HardwareKitAssemblyForm(request.POST or None, hardware_kit=hardwarekit.id)
    part_form = PartHKAssemblyForm(request.POST or None, hardware_kit=hardwarekit.id)
    hk_form = HardwareKitForm(request.POST or None, instance=hardwarekit)

    context = {
        'hardwarekit': hardwarekit,
        'hardware_form': hardware_form,
        'part_form': part_form,
        'hk_form': hk_form,
    }

    return render(request, 'partsdatabase/hardwarekit/hardwarekit_details.html', context)


@login_required
@staff_member_required
def delete_hardwarekit(request, hardwarekit_id):
    hardwarekit = HardwareKit.objects.get(pk=hardwarekit_id)
    messages.error(request, f"{hardwarekit.name} Successfully Deleted")
    hardwarekit.delete()
    return redirect('partsdatabase:hardwarekit')


@login_required
@staff_member_required
def update_hardwarekit(request, hardwarekit_id):
    hardwarekit = HardwareKit.objects.get(pk=hardwarekit_id)
    form = HardwareKitForm(request.POST or None, instance=hardwarekit)

    if request.method == 'POST':
        set_hk = request.POST
        set_hk._mutable = True
        set_hk['name'] = set_hk['name'].upper()
        set_hk._mutable = False

        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data['name']} Successfully Updated")
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


"""
Hardware HK CRUD
"""
@login_required
@staff_member_required
def hardware_hk_form_submit(request, hardwarekit_id):
    hardwarekit = HardwareKit.objects.get(pk=hardwarekit_id)
    form = HardwareKitAssemblyForm(request.POST or None)

    if request.method == 'POST':
        set_hk = request.POST
        set_hk._mutable = True
        set_hk['hardware_kit'] = hardwarekit
        set_hk._mutable = False

        if form.is_valid():
            form.save()
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


@login_required
@staff_member_required
def hardware_hk_form_delete(request, hardwarekit_id, hardware_id):
    hardwarekit_hardware = HardwareKitAssembly.objects.get(pk=hardware_id, hardware_kit=hardwarekit_id)
    hardwarekit_hardware.delete()
    messages.success(request, f"Successfully Removed {hardwarekit_hardware.hardware.name}")
    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


@login_required
@staff_member_required
def hardware_hk_form_edit(request, hardwarekit_id, hardware_id):
    hardwarekit_hardware = HardwareKitAssembly.objects.get(pk=hardware_id, hardware_kit=hardwarekit_id)

    if request.method == 'POST':
        qty = request.POST.get(f"hardware_qty_{hardware_id}", '')

        if int(qty) > 0:
            hardwarekit_hardware.quantity = int(qty)
            hardwarekit_hardware.save()
            messages.success(request, f"Successfully Updated {hardwarekit_hardware.hardware.name}")
        else:
            messages.success(request, f"Successfully Removed {hardwarekit_hardware.hardware.name}")
            hardwarekit_hardware.delete()

    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


"""
Part HK CRUD
"""
@login_required
@staff_member_required
def part_hk_form_submit(request, hardwarekit_id):
    hardwarekit = HardwareKit.objects.get(pk=hardwarekit_id)
    form = PartHKAssemblyForm(request.POST or None)

    if request.method == 'POST':
        set_hk = request.POST
        set_hk._mutable = True
        set_hk['hardware_kit'] = hardwarekit
        set_hk._mutable = False

        if form.is_valid():
            form.save()
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{error}")

    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


@login_required
@staff_member_required
def part_hk_form_delete(request, hardwarekit_id, part_id):
    hardwarekit_part = PartHKAssembly.objects.get(pk=part_id, hardware_kit=hardwarekit_id)
    hardwarekit_part.delete()
    messages.success(request, f"Successfully Updated {hardwarekit_part.part.name}")
    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)


@login_required
@staff_member_required
def part_hk_form_edit(request, hardwarekit_id, part_id):
    hardwarekit_part = PartHKAssembly.objects.get(pk=part_id, hardware_kit=hardwarekit_id)

    if request.method == 'POST':
        qty = request.POST.get(f"part_qty_{part_id}", '')

        if int(qty) > 0:
            hardwarekit_part.quantity = int(qty)
            hardwarekit_part.save()
            messages.success(request, f"Successfully Updated {hardwarekit_part.part.name}")
        else:
            messages.success(request, f"Successfully Removed {hardwarekit_part.part.name}")
            hardwarekit_part.delete()

    return redirect('partsdatabase:details_hardwarekit', hardwarekit_id)
