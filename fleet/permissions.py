from functools import wraps

from django.core.exceptions import PermissionDenied

FLEET_ADMIN_GROUP = "FleetAdmin"


def user_is_fleet_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name=FLEET_ADMIN_GROUP).exists()


def fleet_admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not user_is_fleet_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
