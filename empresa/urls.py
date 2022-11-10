from django.urls import path
from . import views as v

urlpatterns = [
    path('nova_empresa/', v.nova_empresa, name='nova_empresa'),
    path('empresas/', v.empresas, name='empresas'),
    path('excluir_empresa/<int:id>', v.excluir_empresa, name='excluir_empresa'),
]
