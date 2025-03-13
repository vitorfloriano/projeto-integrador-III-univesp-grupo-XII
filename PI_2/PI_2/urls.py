"""
URL configuration for PI_2 project.

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
from django.urls import path, include

urlpatterns = [
    path('AutoItaAdmin/', admin.site.urls),
    path('', include ('app.urls')),
    path('Forms', include ('app.urls')),
    path('Contato', include ('app.urls')),
    path('HomePage', include ('app.urls'))
]

admin.site.site_title = "Administração AutoIta"
admin.site.site_header = "Administração"
admin.site.index_title = "Banco de Dados"