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
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
# Temporarily commenting out this import to fix the startup issue
# from rest_framework.documentation import include_docs_urls

def health_check(request):
    """
    Health check endpoint for Azure App Service monitoring.
    Returns a 200 OK response when the application is healthy.
    """
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('AutoItaAdmin/', admin.site.urls),
    path('', include ('app.urls')),
    path('Forms', include ('app.urls')),
    path('Contato', include ('app.urls')),
    path('HomePage', include ('app.urls')),
    path('api/', include('app.api_urls')),
    path('health/', health_check, name='health_check'),
    # Temporarily disabling API docs until we fix the coreapi issue
    # path('api-docs/', include_docs_urls(title='Autoita API Documentation')),
]

# Add this section to serve static files during development
if settings.DEBUG:
    # Use STATICFILES_DIRS as the document_root since STATIC_ROOT is typically for production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_title = "Administração AutoIta"
admin.site.site_header = "Administração"
admin.site.index_title = "Banco de Dados"