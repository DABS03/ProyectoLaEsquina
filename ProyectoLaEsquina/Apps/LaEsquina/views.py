from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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
        username = request.POST['username'].strip()  # Aplicar trim (strip)
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(usuario=username)
            if user.contrasena == password:
                request.session['user_id'] = user.id_usuario
                request.session['user_role'] = user.id_rol.nombre_rol
                request.session['username'] = user.usuario.strip()  # Aplicar trim al nombre de usuario al almacenarlo

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
        form = CrearCuentaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Cuenta creada exitosamente. Ya puede iniciar sesión.')
            return redirect('login')  
    else:
        form = CrearCuentaForm()
    return render(request, 'crear_cuenta.html', {'form': form})

#@role_required(allowed_roles=['Cliente'])
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
    logout(request) 
    return redirect('login')  
