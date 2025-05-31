from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ViewSets и Views
from drones.views import DroneViewSet, BookingViewSet, UserViewSet
from users.views import RegisterView, UserProfileView
from users.token import MyTokenObtainPairView  # <- обязательно кастомный
from rest_framework_simplejwt.views import TokenRefreshView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger схема
schema_view = get_schema_view(
    openapi.Info(
        title="Drone API",
        default_version='v1',
        description="Документация API аренды дронов",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# DRF роутер
router = DefaultRouter()
router.register(r'drones', DroneViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'users', UserViewSet)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/me/', UserProfileView.as_view(), name='user-profile'),

    # JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # <- кастомный
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # DRF авторизация
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Медиа-файлы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
