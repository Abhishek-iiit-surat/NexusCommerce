from django.urls import path
from .views import PlaceOrderView, MyOrdersView, OrderDetailView, CancelOrderView, AdminUpdateStatusView

urlpatterns = [
    path('', PlaceOrderView.as_view(), name='place-order'),
    path('mine/', MyOrdersView.as_view(), name='my-orders'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('<int:order_id>/status/', AdminUpdateStatusView.as_view(), name='admin-update-status'),
]
