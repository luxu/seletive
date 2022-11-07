from django.shortcuts import render

def nova_empresa(request):
    template_name = 'empresa/nova_empresa.html'
    return render(request, template_name)
