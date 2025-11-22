from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import FloodSite, Uplink


def flood_home(request):
    return render(
        request,
        "flood/home.html",
        {"GOOGLE_MAPS_API_KEY": getattr(settings, "GOOGLE_MAPS_API_KEY", "")},
    )


def flood_plot(request, handle: str):
    site = get_object_or_404(FloodSite, handle=handle)
    return render(request, "flood/plot.html", {"handle": site.handle})


def api_uplinks(request):
    now = timezone.now()
    data: dict[str, dict] = {}
    sites = FloodSite.objects.filter(active=True).prefetch_related("uplinks")
    for site in sites:
        uplink = site.uplinks.order_by("-received_at").first()
        if uplink is None:
            continue
        minutes_since = int((now - uplink.received_at).total_seconds() / 60)
        data[site.handle] = {
            "lat": float(site.latitude),
            "lng": float(site.longitude),
            "location": site.location_description,
            "distance": uplink.distance_mm,
            "battery": uplink.battery_v,
            "signal": uplink.signal_dbm,
            "timestamp": uplink.received_at.isoformat(),
            "minutes_since_last_uplink": minutes_since,
            "level_state": uplink.level_state,
        }
    return JsonResponse(data)


def api_history(request):
    handle = request.GET.get("handle")
    if not handle:
        return JsonResponse({"error": "handle is required"}, status=400)

    days_param = request.GET.get("days") or "7"
    try:
        days = int(days_param)
    except ValueError:
        days = 7

    site = get_object_or_404(FloodSite, handle=handle)
    since = timezone.now() - timedelta(days=days)
    uplinks = (
        site.uplinks.filter(received_at__gte=since)
        .order_by("received_at")
        .only("received_at", "distance_mm")
    )
    history = [
        {"created_at": u.received_at.isoformat(), "distance": u.distance_mm}
        for u in uplinks
    ]
    payload = {
        "site_details": {
            "handle": site.handle,
            "location": site.location_description,
            "lat": float(site.latitude),
            "lng": float(site.longitude),
        },
        "history": history,
    }
    return JsonResponse(payload)

