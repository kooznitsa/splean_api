from django.urls import include, path
from rest_framework import routers

from album.v1 import views

router = routers.DefaultRouter()
router.register('', views.AlbumViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
