from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('myapp.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('fleet/', include(('fleet.urls', 'fleet'), namespace='fleet')),
    path('water/', include(('dwqmp.urls', 'dwqmp'), namespace='dwqmp')),
    path('journeys/', include(('journeys.urls', 'journeys'), namespace='journeys')),
    path('flood/', include(('flood.urls', 'flood'), namespace='flood')),
    path('admin/', admin.site.urls),
]

