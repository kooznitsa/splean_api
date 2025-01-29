from django.urls import include, path
from rest_framework import routers

from song.v1 import views

router = routers.DefaultRouter()
router.register('', views.SongViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
