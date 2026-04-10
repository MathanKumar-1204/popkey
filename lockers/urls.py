from django.urls import path
from .views import LockerListCreateView, LockerDetailView, AvailableLockersView

urlpatterns = [
    path('', LockerListCreateView.as_view(), name='locker-list-create'),
    path('available/', AvailableLockersView.as_view(), name='available-lockers'),
    path('<int:pk>/', LockerDetailView.as_view(), name='locker-detail'),
]
