from django.contrib import admin
from django.urls import path, include
from accounts.views import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/auth/', include('accounts.urls')),
    path('api/lockers/', include('lockers.urls')),
    path('api/reservations/', include('reservations.urls')),
]