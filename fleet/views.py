from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import DefectReportForm, MaintenanceRecordForm, VehicleForm
from .models import DefectReport, MaintenanceRecord, Vehicle


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "fleet/vehicle_list.html", {"vehicles": vehicles})


@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    defects = vehicle.defects.all()
    maintenance = vehicle.maintenance_records.all()
    return render(
        request,
        "fleet/vehicle_detail.html",
        {"vehicle": vehicle, "defects": defects, "maintenance_records": maintenance},
    )


@login_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            return redirect("fleet:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm()
    return render(request, "fleet/vehicle_form.html", {"form": form})


@login_required
def defect_create(request, vehicle_pk=None):
    initial = {}
    if vehicle_pk is not None:
        initial["vehicle"] = get_object_or_404(Vehicle, pk=vehicle_pk)

    if request.method == "POST":
        form = DefectReportForm(request.POST, initial=initial)
        if form.is_valid():
            defect = form.save(commit=False)
            defect.reported_by = request.user
            defect.save()
            return redirect("fleet:vehicle_detail", pk=defect.vehicle.pk)
    else:
        form = DefectReportForm(initial=initial)
    return render(request, "fleet/defect_form.html", {"form": form})


@login_required
def maintenance_create(request, vehicle_pk=None):
    initial = {}
    if vehicle_pk is not None:
        initial["vehicle"] = get_object_or_404(Vehicle, pk=vehicle_pk)

    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST, initial=initial)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            return redirect("fleet:vehicle_detail", pk=record.vehicle.pk)
    else:
        form = MaintenanceRecordForm(initial=initial)
    return render(request, "fleet/maintenance_form.html", {"form": form})


