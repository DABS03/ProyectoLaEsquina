from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario, Rol

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(usuario=username)
            if user.contrasena == password:
                if user.id_rol.nombre_rol == 'Admin':
                    return redirect('admin_view')
                elif user.id_rol.nombre_rol == 'Cliente':
                    return redirect('cliente_view')
                elif user.id_rol.nombre_rol == 'Aseguradora':
                    return redirect('aseguradora_view')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no existe')
    
    return render(request, 'vlogin.html')

def admin_view(request):
    return render(request, 'admin.html')

def cliente_view(request):
    return render(request, 'cliente.html')

def aseguradora_view(request):
    return render(request, 'aseguradora.html')
