from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from .forms import CrearCuentaForm

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.session.get('user_id'):
                return redirect('login')
            user_role = request.session.get('user_role')
            if user_role not in allowed_roles:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(usuario=username)
            if user.contrasena == password:
                request.session['user_id'] = user.id_usuario
                request.session['user_role'] = user.id_rol.nombre_rol
                
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

@role_required(allowed_roles=['Admin'])
def admin_view(request):
    # Obtén todos los pedidos de productos y servicios
    pedidos_productos = PedidoProducto.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario').all()
    pedidos_servicios = PedidoServicio.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario', 'id_servicio').all()
    
    # Obtén todos los usuarios
    usuarios = Usuario.objects.all()
    
    context = {
        'pedidos_productos': pedidos_productos,
        'pedidos_servicios': pedidos_servicios,
        'usuarios': usuarios,
    }
    return render(request, 'admin.html', context)



@role_required(allowed_roles=['Cliente'])
def cliente_view(request):
    return render(request, 'cliente.html')

@role_required(allowed_roles=['Aseguradora'])
def aseguradora_view(request):
    # Obtén el ID del usuario logueado desde la sesión
    user_id = request.session.get('user_id')
    
    # Filtra los servicios basándote en el usuario logueado
    servicios = PedidoServicio.objects.filter(id_pedido__id_usuario=user_id)
    
    # Pasar los servicios al template
    context = {
        'servicios': servicios,
    }
    
    return render(request, 'aseguradora.html', context)

def crear_cuenta(request):
    if request.method == 'POST':
        form = CrearCuentaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guardar en base de datos
            return redirect('login')  # Redirigir a la página de login después de crear la cuenta
    else:
        form = CrearCuentaForm()
    return render(request, 'crear_cuenta.html', {'form': form})

@role_required(allowed_roles=['Cliente'])
def cliente_view(request):
    # Obtener todos los productos y servicios
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()

    # Pasar los productos y servicios al template
    context = {
        'productos': productos,
        'servicios': servicios,
    }
    return render(request, 'cliente.html', context)
