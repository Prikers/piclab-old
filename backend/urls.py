from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api import views as api_views
from .user import views as user_views

router = routers.DefaultRouter()
router.register('photos', api_views.PhotoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # User registration
    path('api/register/', user_views.RegisterView.as_view(), name='register'),
    # Router 
    path('api/', include(router.urls)),
]
