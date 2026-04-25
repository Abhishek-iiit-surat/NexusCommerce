from django.urls import path
from .views import (
    RegisterView, 
    LoginView,
    GetUserDetailsView,
    HealthCheckView,
    LogoutView,
    RefreshTokenView,
    UpdateUserView,
    ResetPasswordView,
    DeleteUserView
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('get-user-details/', GetUserDetailsView.as_view(), name='get-user-details'),
    path('health-check/', HealthCheckView.as_view(), name='health-check'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
