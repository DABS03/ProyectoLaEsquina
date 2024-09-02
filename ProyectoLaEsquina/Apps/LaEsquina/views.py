'''from django.shortcuts import render
from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("Hola mundo")'''

from django.shortcuts import render
from .models import EstadoPedido

def hola_mundo(request):
    estados = EstadoPedido.objects.all()  # Obtiene todos los estados de pedido
    return render(request, 'lista_estados.html', {'estados': estados})
