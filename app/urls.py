from django.urls import path
from . import views

urlpatterns = [
    # Primary routes with standardized lowercase names
    path('', views.homepage, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('contato/', views.contatos, name='contato'),
    path('forms/', views.form, name='formulario'),
    
    # Kept for backward compatibility, but redirecting to proper URLs
    path('Homepage', views.homepage, name='homepage_redirect'),
    path('Contato', views.contatos, name='contato_redirect'),
    path('Forms', views.form, name='form_redirect'),
    path('catalogo', views.catalogo, name='catalogo_no_slash'),
    
    # Test route
    path('test/', views.test_view, name='test_view'),
]

