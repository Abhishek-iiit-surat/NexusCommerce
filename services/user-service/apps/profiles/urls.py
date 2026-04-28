from django.urls import path

from .views import (
    ProfileView,
    AddressListCreateView,
    AddressDetailView,
    AddressSetDefaultView,
    InternalProfileView,
    HealthCheckView,
)

urlpatterns = [
    path('me/', ProfileView.as_view(), name='profile-me'),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:address_id>/', AddressDetailView.as_view(), name='address-detail'),
    path('addresses/<int:address_id>/set-default/', AddressSetDefaultView.as_view(), name='address-set-default'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('internal/profiles/<int:user_id>/', InternalProfileView.as_view(), name='internal-profile'),

]
