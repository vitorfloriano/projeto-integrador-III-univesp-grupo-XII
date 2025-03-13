from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('Contato', views.contatos, name='contatos'),
    path('Forms', views.form, name='form'),
    path('Homepage', views.homepage)
    ]

    