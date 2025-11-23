from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DefectReportForm, MaintenanceRecordForm, VehicleForm
from .models import DefectReport, MaintenanceEvidence, MaintenanceRecord, Vehicle


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "fleet/vehicle_list.html", {"vehicles": vehicles})


@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    defects = vehicle.defects.select_related("reported_by")
    maintenance = vehicle.maintenance_records.select_related(
        "submitted_by", "defect_report"
    ).prefetch_related("evidence_documents")
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
def defect_detail(request, pk):
    defect = get_object_or_404(
        DefectReport.objects.select_related("vehicle", "reported_by").prefetch_related(
            "maintenance_records__submitted_by"
        ),
        pk=pk,
    )
    return render(request, "fleet/defect_detail.html", {"defect": defect})


@login_required
def defect_update(request, pk):
    defect = get_object_or_404(DefectReport, pk=pk)
    if request.method == "POST":
        form = DefectReportForm(request.POST, instance=defect)
        if form.is_valid():
            form.save()
            return redirect("fleet:defect_detail", pk=defect.pk)
    else:
        form = DefectReportForm(instance=defect)
    return render(
        request,
        "fleet/defect_form.html",
        {
            "form": form,
            "form_title": "Edit defect",
            "submit_label": "Update defect",
        },
    )


@login_required
def maintenance_create(request, vehicle_pk=None):
    vehicle = None
    if vehicle_pk is not None:
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    initial = {"vehicle": vehicle} if vehicle else {}

    if request.method == "POST":
        form = MaintenanceRecordForm(
            request.POST, request.FILES, initial=initial, vehicle=vehicle
        )
        if form.is_valid():
            record = form.save(commit=False)
            record.submitted_by = request.user
            record.save()
            _save_record_evidence(record, request.FILES.getlist("evidence_files"), request.user)
            return redirect("fleet:vehicle_detail", pk=record.vehicle.pk)
    else:
        form = MaintenanceRecordForm(initial=initial, vehicle=vehicle)
    return render(request, "fleet/maintenance_form.html", {"form": form})


@login_required
def maintenance_detail(request, pk):
    record = get_object_or_404(
        MaintenanceRecord.objects.select_related(
            "vehicle", "submitted_by", "defect_report"
        ).prefetch_related("evidence_documents__uploaded_by"),
        pk=pk,
    )
    return render(request, "fleet/maintenance_detail.html", {"record": record})


@login_required
def maintenance_update(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)
    vehicle = record.vehicle
    if request.method == "POST":
        form = MaintenanceRecordForm(
            request.POST, request.FILES, instance=record, vehicle=vehicle
        )
        if form.is_valid():
            record = form.save(commit=False)
            record.submitted_by = request.user
            record.save()
            _save_record_evidence(record, request.FILES.getlist("evidence_files"), request.user)
            return redirect("fleet:maintenance_detail", pk=record.pk)
    else:
        form = MaintenanceRecordForm(instance=record, vehicle=vehicle)
    return render(
        request,
        "fleet/maintenance_form.html",
        {
            "form": form,
            "form_title": "Edit maintenance record",
            "submit_label": "Update record",
        },
    )


def _save_record_evidence(record, files, user):
    for upload in files or []:
        if not upload:
            continue
        MaintenanceEvidence.objects.create(
            maintenance_record=record,
            file=upload,
            uploaded_by=user if user.is_authenticated else None,
        )
