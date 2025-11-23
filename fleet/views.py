from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DefectReportForm, MaintenanceRecordForm, VehicleForm
from .models import DefectReport, MaintenanceEvidence, MaintenanceRecord, Vehicle
from .permissions import fleet_admin_required, user_is_fleet_admin


@login_required
def defect_list(request):
    can_manage = user_is_fleet_admin(request.user)
    defects_qs = (
        DefectReport.objects.filter(status__in=["open", "in_progress"])
        .select_related("vehicle", "reported_by")
        .order_by("-reported_at")
    )
    paginator = Paginator(defects_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "fleet/defect_list.html",
        {"page_obj": page_obj, "defects": page_obj.object_list, "can_manage_fleet": can_manage},
    )


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    can_manage = user_is_fleet_admin(request.user)
    return render(
        request,
        "fleet/vehicle_list.html",
        {"vehicles": vehicles, "can_manage_fleet": can_manage},
    )


@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    defects = vehicle.defects.select_related("reported_by")
    maintenance = vehicle.maintenance_records.select_related(
        "submitted_by", "defect_report"
    ).prefetch_related("evidence_documents")
    can_manage = user_is_fleet_admin(request.user)
    return render(
        request,
        "fleet/vehicle_detail.html",
        {
            "vehicle": vehicle,
            "defects": defects,
            "maintenance_records": maintenance,
            "can_manage_fleet": can_manage,
        },
    )


@login_required
@fleet_admin_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            return redirect("fleet:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm()
    return render(
        request,
        "fleet/vehicle_form.html",
        {"form": form, "form_title": "Add vehicle"},
    )


@login_required
@fleet_admin_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("fleet:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(
        request,
        "fleet/vehicle_form.html",
        {"form": form, "form_title": "Edit vehicle", "submit_label": "Update vehicle"},
    )


@login_required
@fleet_admin_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        vehicle.delete()
        return redirect("fleet:vehicle_list")
    return render(
        request,
        "fleet/vehicle_confirm_delete.html",
        {"vehicle": vehicle},
    )


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
    can_manage = user_is_fleet_admin(request.user)
    return render(
        request,
        "fleet/defect_detail.html",
        {"defect": defect, "can_manage_fleet": can_manage},
    )


@login_required
@fleet_admin_required
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
@fleet_admin_required
def maintenance_create(request, vehicle_pk=None):
    vehicle = None
    if vehicle_pk is not None:
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    defect = None
    defect_pk = request.GET.get("defect")
    if defect_pk:
        defect = get_object_or_404(DefectReport, pk=defect_pk)
        if vehicle is None:
            vehicle = defect.vehicle
    initial = {}
    if vehicle:
        initial["vehicle"] = vehicle
    if defect:
        initial["defect_report"] = defect

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
    return render(
        request,
        "fleet/maintenance_form.html",
        {"form": form, "form_title": "Add maintenance record"},
    )


@login_required
def maintenance_detail(request, pk):
    record = get_object_or_404(
        MaintenanceRecord.objects.select_related(
            "vehicle", "submitted_by", "defect_report"
        ).prefetch_related("evidence_documents__uploaded_by"),
        pk=pk,
    )
    can_manage = user_is_fleet_admin(request.user)
    return render(
        request,
        "fleet/maintenance_detail.html",
        {"record": record, "can_manage_fleet": can_manage},
    )


@login_required
@fleet_admin_required
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
