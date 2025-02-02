"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('v1/albums/', include('album.v1.urls')),
    path('v1/songs/', include('song.v1.urls')),
    path('v1/lines/', include('line.v1.urls')),

    # -------------------------- Swagger ---------------------------------
    path('v1/swagger_yml/', SpectacularAPIView.as_view(api_version='v1'), name='schema-v1'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema-v1'), name='swagger-v1'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('v1/redoc/', SpectacularRedocView.as_view(url_name='schema-v1'), name='redoc-v1'),
]
