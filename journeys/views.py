from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import CheckpointForm, JourneyForm
from .models import Checkpoint, Journey


@login_required
def journey_list(request):
    journeys = Journey.objects.filter(
        Q(driver=request.user) | Q(buddy=request.user) | Q(created_by=request.user)
    ).select_related("driver", "buddy", "vehicle")
    return render(request, "journeys/journey_list.html", {"journeys": journeys})


@login_required
def journey_detail(request, pk):
    journey = get_object_or_404(
        Journey.objects.select_related("driver", "buddy", "vehicle"), pk=pk
    )
    checkpoints = journey.checkpoints.all()
    return render(
        request,
        "journeys/journey_detail.html",
        {"journey": journey, "checkpoints": checkpoints},
    )


@login_required
def journey_create(request):
    if request.method == "POST":
        form = JourneyForm(request.POST)
        if form.is_valid():
            journey = form.save(commit=False)
            journey.created_by = request.user
            journey.status = "active"
            journey.save()
            return redirect("journeys:journey_detail", pk=journey.pk)
    else:
        form = JourneyForm(initial={"driver": request.user})
    return render(request, "journeys/journey_form.html", {"form": form})


@login_required
def checkpoint_create(request, journey_pk):
    journey = get_object_or_404(Journey, pk=journey_pk)
    if request.method == "POST":
        form = CheckpointForm(request.POST)
        if form.is_valid():
            checkpoint = form.save(commit=False)
            checkpoint.journey = journey
            checkpoint.save()
            return redirect("journeys:journey_detail", pk=journey.pk)
    else:
        agg = journey.checkpoints.aggregate(Max("sequence"))
        next_seq = (agg.get("sequence__max") or 0) + 1
        form = CheckpointForm(initial={"sequence": next_seq})
    return render(
        request,
        "journeys/checkpoint_form.html",
        {"form": form, "journey": journey},
    )


@login_required
def checkpoint_checkin(request, checkpoint_uuid):
    checkpoint = get_object_or_404(Checkpoint, uuid=checkpoint_uuid)
    if request.method == "POST":
        checkpoint.checked_in_at = timezone.now()
        checkpoint.checked_in_by = request.user
        checkpoint.save()
        return redirect("journeys:journey_detail", pk=checkpoint.journey.pk)
    return render(
        request,
        "journeys/checkpoint_checkin.html",
        {"checkpoint": checkpoint},
    )

