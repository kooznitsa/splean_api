from django.urls import include, path
from rest_framework import routers

from line.v1 import views

router = routers.DefaultRouter()
router.register('', views.LineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
