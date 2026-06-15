from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.cart.views import InternalCartView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include('apps.cart.urls')),
    path('internal/cart/<int:user_id>/', InternalCartView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
