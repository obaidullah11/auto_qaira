from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .swagger import schema_view
from rest_framework_simplejwt .views import(TokenObtainPairView,TokenRefreshView)


urlpatterns = [
    # Swagger UI endpoint - API documentation interface
    path('', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    
    path('api/', include('users.urls')),
    # path('api/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('car_onboarding.urls')),
    path('api/', include('reels_management.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)