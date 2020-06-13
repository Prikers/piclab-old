from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .api import views

router = routers.DefaultRouter()
router.register(r'photos', views.PhotoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
