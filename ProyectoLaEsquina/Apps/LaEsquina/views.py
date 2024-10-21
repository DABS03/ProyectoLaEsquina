from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import CrearCuentaForm
from django.contrib.auth import logout as auth_logout
import requests
from django.shortcuts import redirect
from urllib.parse import urlencode
from allauth.socialaccount.models import SocialAccount



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
    # Lógica para inicio de sesión con usuario y contraseña
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if username and password:
            try:
                user = Usuario.objects.get(usuario=username)
                if user.contrasena == password:
                    # Iniciar sesión en la sesión de Django
                    request.session['user_id'] = user.id_usuario
                    request.session['user_role'] = user.id_rol.nombre_rol
                    request.session['username'] = user.usuario.strip()

                    # Redirigir a la vista correspondiente según el rol
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


def google_login(request):
    google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': '594841376131-ltsbl6ovami2ocqhfbstc0nfq6da33td.apps.googleusercontent.com',
        'redirect_uri': 'http://127.0.0.1:8000/oauth2callback/',  # Debe coincidir con tu configuración en Google
        'response_type': 'code',
        'scope': 'email profile',
    }
    url = f"{google_auth_url}?{urlencode(params)}"
    return redirect(url)

def oauth2callback(request):
    code = request.GET.get('code')
    token_url = 'https://oauth2.googleapis.com/token'

    # Intercambia el código por un token de acceso
    response = requests.post(token_url, data={
        'code': code,
        'client_id': '594841376131-ltsbl6ovami2ocqhfbstc0nfq6da33td.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': 'http://127.0.0.1:8000/oauth2callback/',
        'grant_type': 'authorization_code',
    })
    
    # Maneja la respuesta
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')

        # Usa el token de acceso para obtener la información del usuario
        user_info_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            email = user_info.get('email', '').strip().lower()

            try:
                usuario = Usuario.objects.get(correo__iexact=email)  # Busca el usuario en tu tabla 'usuario' basado en el correo
                
                # Guardar la información de la sesión
                request.session['user_id'] = usuario.id_usuario
                request.session['user_role'] = usuario.id_rol.nombre_rol
                request.session['username'] = usuario.usuario.strip()

                # Redirigir según el rol del usuario
                if usuario.id_rol.nombre_rol == 'Admin':
                    return redirect('admin_view')
                elif usuario.id_rol.nombre_rol == 'Cliente':
                    return redirect('cliente_view')
                elif usuario.id_rol.nombre_rol == 'Aseguradora':
                    return redirect('aseguradora_view')
            except Usuario.DoesNotExist:
                messages.error(request, 'El correo autenticado con Google no está registrado en el sistema.')
                return redirect('login')   

        else:
            messages.error(request, 'Error al obtener información del usuario de Google.')
            return redirect('login')
    else:
        messages.error(request, 'Error al autenticar con Google.')
        return redirect('login')
    

def logout_view(request):
    # Cerrar sesión en Django y también en Google
    auth_logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

@role_required(allowed_roles=['Admin'])
def admin_view(request):
    pedidos_productos = PedidoProducto.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario').all()
    pedidos_servicios = PedidoServicio.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario', 'id_servicio').all()
    
 
    usuarios = Usuario.objects.all()
    
    context = {
        'pedidos_productos': pedidos_productos,
        'pedidos_servicios': pedidos_servicios,
        'usuarios': usuarios,
    }
    return render(request, 'admin.html', context)

@role_required(allowed_roles=['Admin'])
def ver_inventario(request):
    productos = Producto.objects.all()  
    return render(request, 'ver_inventario.html', {'productos': productos})

@role_required(allowed_roles=['Admin'])
def edit_pro(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    if request.method == 'POST':
        # Procesar los datos del formulario
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        # Actualizar los campos del producto
        producto.nombre_producto = nombre
        producto.precio = precio
        producto.cantidad_stock = cantidad
        producto.id_categoria_producto_id = categoria
        producto.descripcion = descripcion
        
        # Actualizar imagen solo si se subió una nueva
        if imagen:
            producto.imagen = imagen
        
        producto.save()  # Guardar los cambios en la base de datos
        return redirect('ver_inventario')  # Cambia esto por el nombre de la vista deseada

    return render(request, 'edit_pro.html', {'producto': producto, 'categorias': CategoriaProducto.objects.all()})


@role_required(allowed_roles=['Admin'])
def agregar_pro(request):
    categorias = CategoriaProducto.objects.all()  
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        categoria_id = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')  

        # verificar que todos los campos necesarios estén presentes y no vacíos
        if not all([nombre, precio, cantidad, categoria_id, descripcion]):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return render(request, 'agregar_pro.html', {'categorias': categorias})

        try:
            # validar que precio y cantidad sean valores numéricos
            precio = float(precio)
            cantidad = int(cantidad)
            if precio <= 0 or cantidad <= 0:
                messages.error(request, 'El precio y la cantidad deben ser valores positivos.')
                return render(request, 'agregar_pro.html', {'categorias': categorias})
        except ValueError:
            messages.error(request, 'El precio debe ser un número decimal y la cantidad un número entero.')
            return render(request, 'agregar_pro.html', {'categorias': categorias})

        try:
            categoria = CategoriaProducto.objects.get(id_categoria_producto=categoria_id)

            # Crear el nuevo producto
            nuevo_producto = Producto(
                nombre_producto=nombre,
                precio=precio,
                cantidad_stock=cantidad,
                id_categoria_producto=categoria,
                descripcion=descripcion,
                imagen=imagen  
            )
            nuevo_producto.save()  
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('ver_inventario')  
        except CategoriaProducto.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado: {str(e)}')

    return render(request, 'agregar_pro.html', {'categorias': categorias})

def cliente_view(request):
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()

    is_cliente = request.session.get('user_role') == 'Cliente'  

    context = {
        'productos': productos,
        'servicios': servicios,
        'is_cliente': is_cliente,  
    }
    return render(request, 'cliente.html', context)

def producto_view(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    is_cliente = request.session.get('user_role') == 'Cliente'  

    return render(request, 'v_producto.html', {
        'producto': producto,
        'is_cliente': is_cliente,  
    })


@role_required(allowed_roles=['Aseguradora'])
def aseguradora_view(request):
    user_id = request.session.get('user_id')
    
    servicios = PedidoServicio.objects.filter(id_pedido__id_usuario=user_id)
    
    context = {
        'servicios': servicios,
    }
    
    return render(request, 'aseguradora.html', context)

def crear_cuenta(request):
    if request.method == 'POST':
        form = CrearCuentaForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            rol_cliente = Rol.objects.get(nombre_rol='Cliente')
            usuario.id_rol = rol_cliente
            usuario.save()
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('login')

    else:
        form = CrearCuentaForm()

    return render(request, 'crear_cuenta.html', {'form': form})

def cliente_view(request):

    productos = Producto.objects.all()
    servicios = Servicio.objects.all()

    context = {
        'productos': productos,
        'servicios': servicios,
    }
    return render(request, 'cliente.html', context)

from django.contrib.auth import logout

def logout_view(request):
    # Cerrar sesión en Django y también en Google
    auth_logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')
