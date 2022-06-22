from django.shortcuts import render
from django.contrib import messages
from .models import SIM, Phone, Tablet, OtherDevice
from .forms import (
    DeviceTypeForm,
    PhoneForm,
    SIMForm,
    TabletForm,
    OtherDeviceForm)
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat


def inventory_list(request):
    """Gives a list of all hardware registered."""

    device_type = request.GET.get("options-outlined", "")

    search_query = request.GET.get("search_query", "")

    devices = {}

    if device_type or search_query:
        devices = search_devices(device_type, search_query)

    context = {
        "devices": devices,
        "device_type": device_type,
    }

    return render(request, 'inventory/inventoryList.html', context)


def device_type_list(request):
    """Give a list of devices to be added."""

    form = None
    device_type_form = DeviceTypeForm()

    if request.method == 'POST':

        form = get_device_form(request)

        context = {
            'form': form,
        }

        return render(request, 'inventory/newDeviceForm.html', context)

    context = {
        'device_type_form': device_type_form,
        'form': form,
    }

    return render(request, 'inventory/deviceTypeList.html', context)


def edit_device(request, id, device_type):
    """ Edit device. """

    form = None

    if device_type == 'phone':
        device = Phone.objects.get(pk=id)
        form = PhoneForm(request.POST or None, instance=device)

    elif device_type == 'tablet':
        device = Tablet.objects.get(pk=id)
        form = TabletForm(request.POST or None, instance=device)

    elif device_type == 'sim':
        device = SIM.objects.get(pk=id)
        form = SIMForm(request.POST or None, instance=device)

    elif device_type == 'other_device':
        device = OtherDevice.objects.get(pk=id)
        form = OtherDeviceForm(request.POST or None, instance=device)
    if request.method == 'POST':
        if form.is_valid():
            update_sim_owner(request)
            form.save()
            messages.success(request, 'Device updated successfully!')
        else:
            messages.error(
                request, """Something went wrong. If the problem
                    persists contact support.""")

    context = {
        "form": form,
        "device_type": device_type,
        "device": device
    }

    return render(request, 'inventory/editDeviceForm.html', context)


def delete_device(request, id, device_type):
    """Deletes a device from the inventory"""

    if device_type == 'phone':
        device = Phone.objects.get(pk=id)
        device.delete()
        messages.success(request, 'Phone deleted successfully!')

    if device_type == 'tablet':
        device = Tablet.objects.get(pk=id)
        device.delete()
        messages.success(request, 'Tablet deleted successfully!')

    if device_type == 'sim':
        device = SIM.objects.get(pk=id)
        device.delete()
        messages.success(request, 'SIM deleted successfully!')

    if device_type == 'other_device':
        device = OtherDevice.objects.get(pk=id)
        device.delete()
        messages.success(request, 'Device deleted successfully!')

    return render(request, 'inventory/inventoryList.html')


def get_device_form(request):
    """Returns a form according to what's selected in device list"""

    device_type = request.POST.get('device_type')

    if device_type == 'phone':
        request.session['device_type'] = device_type
        return PhoneForm()
    elif device_type == 'tablet':
        request.session['device_type'] = device_type
        return TabletForm()
    elif device_type == 'sim':
        request.session['device_type'] = device_type
        return SIMForm()
    elif device_type == 'other_device':
        request.session['device_type'] = device_type
        return OtherDeviceForm()


def get_submited_form(request):
    """Returns the form that was submited"""

    device_type = request.session['device_type']

    if device_type == 'phone':
        return PhoneForm(request.POST)
    elif device_type == 'sim':
        return SIMForm(request.POST)
    elif device_type == 'tablet':
        return TabletForm(request.POST)
    elif device_type == 'other_device':
        return OtherDeviceForm(request.POST)


def add_new_device(request):
    """Adds a new device to the inventory"""

    form = get_submited_form(request)

    if form.is_valid():
        form.save(commit=False)
        form.instance.created_by = request.user

        # If phone or tablet, assigns the SIM to the selected employee
        if (request.session['device_type'] == 'phone' or
                request.session['device_type'] == 'tablet'):
            update_sim_owner(request)
        form.save()

        messages.success(request, 'Device added successfully!')
        return render(request, 'inventory/inventoryList.html')
    else:
        messages.error(
            request, """Something went wrong. If the problem
                    persists contact support.""")
    return render(request, 'inventory/newDeviceForm.html', {'form': form})


def update_sim_owner(request):
    """Updates the owner of a SIM"""

    if request.POST.get("assigned_to") and request.POST.get("sim"):
        sim = SIM.objects.get(pk=request.POST.get('sim'))
        sim.assigned_to_id = request.POST.get('assigned_to')
        sim.save()


def search_devices(device_type, search_query):
    """Search for devices"""

    devices = None

    if device_type == 'phone':
        devices = Phone.objects.annotate(
            full_name=Concat('assigned_to__first_name',
                             V(' '), 'assigned_to__last_name')
        ).filter(
            Q(assigned_to__first_name=search_query) |
            Q(assigned_to__last_name=search_query) |
            Q(full_name=search_query) |
            Q(imei=search_query) |
            Q(status=search_query) |
            Q(serial_number__icontains=search_query)
        )

    elif device_type == 'tablet':

        devices = Tablet.objects.annotate(
            full_name=Concat('assigned_to__first_name',
                             V(' '), 'assigned_to__last_name')
        ).filter(
            Q(assigned_to__first_name=search_query) |
            Q(assigned_to__last_name=search_query) |
            Q(full_name=search_query) |
            Q(imei=search_query) |
            Q(status=search_query) |
            Q(serial_number__icontains=search_query)
        )

    elif device_type == 'sim':
        devices = SIM.objects.annotate(
            full_name=Concat('assigned_to__first_name',
                             V(' '), 'assigned_to__last_name')
        ).filter(
            Q(assigned_to__first_name=search_query) |
            Q(assigned_to__last_name=search_query) |
            Q(full_name=search_query) |
            Q(serial_number__icontains=search_query)
        )

    elif device_type == 'other_device':
        devices = OtherDevice.objects.annotate(
            full_name=Concat('assigned_to__first_name',
                             V(' '), 'assigned_to__last_name')
        ).filter(
            Q(assigned_to__first_name=search_query) |
            Q(assigned_to__last_name=search_query) |
            Q(full_name=search_query) |
            Q(serial_number__icontains=search_query)
        )

    return devices
