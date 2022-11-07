from django.urls import path
from . import views as v

urlpatterns = [
    path('nova_empresa/', v.nova_empresa, name='nova_empresa')
]
