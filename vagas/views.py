from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from empresa.models import Vagas
from vagas.models import Tarefa, Emails


def nova_vaga(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        email = request.POST.get('email')
        tecnologias_domina = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_domina = request.POST.getlist('tecnologias_nao_domina')
        experiencia = request.POST.get('experiencia')
        data_final = request.POST.get('data_final')
        empresa = request.POST.get('empresa')
        status = request.POST.get('status')

        vaga = Vagas(
            titulo=titulo,
            email=email,
            nivel_experiencia=experiencia,
            data_final=data_final,
            empresa_id=empresa,
            status=status,
        )
        vaga.save()
        vaga.tecnologias_estudar.add(*tecnologias_nao_domina)
        vaga.tecnologias_dominadas.add(*tecnologias_domina)
        vaga.save()
        messages.add_message(request, constants.SUCCESS, 'Vaga criada com sucesso.')
        return redirect(f'/home/empresa/{empresa}')
    elif request.method == "GET":
        raise Http404()


def vaga(request, id):
    template_name = 'vagas/vaga.html'
    vaga = get_object_or_404(Vagas, id=id)
    tarefas = Tarefa.objects.filter(vaga=vaga).filter(realizada=False)
    emails = Emails.objects.filter(vaga=vaga)
    context = {
        'vaga': vaga,
        'tarefas': tarefas,
        'emails': emails
    }
    return render(request, template_name, context)


def nova_tarefa(request, id_vaga):
    titulo = request.POST.get('titulo')
    prioridade = request.POST.get("prioridade")
    data = request.POST.get('data')
    tarefa = Tarefa(
        vaga_id=id_vaga,
        titulo=titulo,
        prioridade=prioridade,
        data=data
    )
    tarefa.save()
    messages.add_message(request, constants.SUCCESS, 'Tarefa criada com sucesso')
    return redirect(f'/vagas/vaga/{id_vaga}')


def realizar_tarefa(request, id):
    tarefas_list = Tarefa.objects.filter(id=id).filter(realizada=False)

    if not tarefas_list.exists():
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
        return redirect('/home/empresas/')

    tarefa = tarefas_list.first()
    tarefa.realizada = True
    tarefa.save()
    messages.add_message(request, constants.SUCCESS, 'Tarefa realizada com sucesso, parabéns!')
    return redirect(f'/vagas/vaga/{tarefa.vaga.id}')


def envia_email(request, id_vaga):
    vaga = Vagas.objects.get(id=id_vaga)
    assunto = request.POST.get('assunto')
    corpo = request.POST.get('corpo')
    template_name = 'emails/template_email.html'
    context = {
        'corpo': corpo
    }

    email_content = [vaga.email, ]
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        assunto,
        text_content,
        settings.EMAIL_HOST_USER,
        email_content
    )
    email.attach_alternative(html_content, "text/html")
    if email.send():
        mail = Emails(
            vaga=vaga,
            assunto=assunto,
            corpo=corpo,
            enviado=True
        )
        messages.add_message(request, constants.SUCCESS, 'Email enviado com sucesso.')
    else:
        mail = Emails(
            vaga=vaga,
            assunto=assunto,
            corpo=corpo,
            enviado=False
        )
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
    mail.save()
    return redirect(f'/vagas/vaga/{id_vaga}')
