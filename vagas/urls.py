from django.urls import path

from . import views as v

urlpatterns = [
    path("nova_vaga/", v.nova_vaga, name="nova_vaga"),
    path('vaga/<int:id>', v.vaga, name="vaga"),
    path('nova_tarefa/<int:id_vaga>', v.nova_tarefa, name='nova_tarefa'),
    path('realizar_tarefa/<int:id>', v.realizar_tarefa, name='realizar_tarefa'),
    path('envia_email/<int:id_vaga>', v.envia_email, name="envia_email")
]