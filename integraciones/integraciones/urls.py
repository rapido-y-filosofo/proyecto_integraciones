"""integraciones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from backend_integraciones import views as vv
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_api_mercado_publico', vv.test_api_mercado_publico),
    path('licitaciones_hoy', vv.licitaciones_por_fecha),
    path('test_query', vv.get_sample_licitaciones),
]
