from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import CrearCuentaForm
from django.contrib.auth import logout as auth_logout
import requests
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from .models import *

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

################################
################################
# INICIO ADMIN

@role_required(allowed_roles=['Admin'])
def admin_view(request):
    # Obtener los pedidos de productos y servicios como antes
    pedidos_productos = (
        PedidoProducto.objects
        .select_related('id_pedido__id_estado', 'id_pedido__id_usuario')
        .values('id_pedido')
        .annotate(total_subtotal=Sum('subtotal'))
    )

    pedidos = []
    for pedido in pedidos_productos:
        pedido_info = Pedido.objects.get(id_pedido=pedido['id_pedido'])
        pedidos.append({
            'id_pedido': pedido_info.id_pedido,
            'nombre_cliente': pedido_info.id_usuario.nombres,
            'comentarios': pedido_info.comentarios,
            'fecha_pedido': pedido_info.fecha_pedido,
            'subtotal': pedido['total_subtotal'],
            'estado': pedido_info.id_estado.nombre_estado,
        })

    pedidos_servicios = PedidoServicio.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario', 'id_servicio').all()

    # Obtener las sugerencias de los clientes
    sugerencias = Sugerencia.objects.select_related('id_usuario').all()

    # Contexto para la plantilla
    context = {
        'pedidos_productos': pedidos,
        'pedidos_servicios': pedidos_servicios,
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias],
    }
    return render(request, 'admin.html', context)


@role_required(allowed_roles=['Admin'])
def ver_inventario(request):
    productos = Producto.objects.all()
    sugerencias = Sugerencia.objects.select_related('id_usuario').all()
    return render(request, 'ver_inventario.html', {
        'productos': productos, 
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias]
    })

@role_required(allowed_roles=['Admin'])
def edit_pro(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    sugerencias = Sugerencia.objects.select_related('id_usuario').all()
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

    return render(request, 'edit_pro.html', {
        'producto': producto, 
        'categorias': CategoriaProducto.objects.all(), 
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias]
    })


@role_required(allowed_roles=['Admin'])
def agregar_pro(request):
    categorias = CategoriaProducto.objects.all()  
    sugerencias = Sugerencia.objects.select_related('id_usuario').all()
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

    return render(request, 'agregar_pro.html', {
        'categorias': categorias,
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias]})

@role_required(allowed_roles=['Admin'])
def historial_pedidos(request):
    # Obtener todos los pedidos y sus productos
    pedidos_productos = PedidoProducto.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario', 'id_producto').all()

    # Agrupar los pedidos por id_pedido y calcular el subtotal
    historial = {}
    for pedido_producto in pedidos_productos:
        pedido_id = pedido_producto.id_pedido.id_pedido
        if pedido_id not in historial:
            historial[pedido_id] = {
                'pedido': pedido_producto.id_pedido,
                'productos': [],
                'subtotal': 0  # Inicializa subtotal
            }
        historial[pedido_id]['productos'].append(pedido_producto)
        historial[pedido_id]['subtotal'] += pedido_producto.subtotal  # Acumula el subtotal

        sugerencias = Sugerencia.objects.select_related('id_usuario').all()

    context = {
        'historial': historial,
        'estados': EstadoPedido.objects.all(),  # Asegúrate de incluir los estados aquí
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias],
    }
    return render(request, 'v_historialpedidos.html', context)

#Cambiar estado para historial de pedido
@role_required(allowed_roles=['Admin'])
def cambiar_estado(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
        nuevo_estado_id = request.POST.get('estado')
        nuevo_estado = get_object_or_404(EstadoPedido, id_estado=nuevo_estado_id)
        
        pedido.id_estado = nuevo_estado
        pedido.save()
        
        # Redirige de vuelta a la página de pedidos o donde necesites
        return redirect('historial_pedidos')  


@role_required(allowed_roles=['Admin'])
def historial_solicitudes(request):
    pedidos_servicios = PedidoServicio.objects.select_related('id_pedido__id_estado', 'id_pedido__id_usuario', 'id_servicio').all()
    usuarios = Usuario.objects.all()
    estados = EstadoPedido.objects.all()  # Obtener todos los estados
    sugerencias = Sugerencia.objects.select_related('id_usuario').all()
    context = {
        'pedidos_servicios': pedidos_servicios,
        'usuarios': usuarios,
        'estados': estados,  # Pasar los estados al contexto
        'sugerencias': [{'nombre_cliente': sug.id_usuario.nombres, 'mensaje': sug.mensaje} for sug in sugerencias],
    }
    return render(request, 'v_solicitudes.html', context)

# Cambiar estado para las solicitudes
@role_required(allowed_roles=['Admin'])
def cambiar_estado_solicitud(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
        nuevo_estado_id = request.POST.get('estado')
        nuevo_estado = get_object_or_404(EstadoPedido, id_estado=nuevo_estado_id)
        
        pedido.id_estado = nuevo_estado
        pedido.save()
        
        # Redirige a la vista de solicitudes
        return redirect('historial_solicitudes')


# FIN ADMIN
################################
################################

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

# INICIO Carrito


@role_required(allowed_roles=['Cliente'])
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))  # Obtener la cantidad seleccionada
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, 'Debe iniciar sesión para agregar productos al carrito.')
            return redirect('login')

        producto = get_object_or_404(Producto, id_producto=producto_id)

        # Obtener o crear el carrito del usuario
        carrito, created = Carrito.objects.get_or_create(id_usuario_id=user_id)

        # Verificar si el producto ya está en el carrito
        item_carrito, item_created = ItemsCarrito.objects.get_or_create(
            id_carrito=carrito,
            id_producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio': producto.precio,
                'subtotal': producto.precio * cantidad
            }
        )

        # Si ya existía, solo actualiza la cantidad y el subtotal
        if not item_created:
            item_carrito.cantidad += cantidad
            item_carrito.subtotal = item_carrito.cantidad * item_carrito.precio
            item_carrito.save()


        
        return redirect('cliente_view')

    return redirect('cliente_view')

@role_required(allowed_roles=['Cliente'])
def mi_carrito_view(request):
    user_id = request.session.get('user_id')
    carrito = Carrito.objects.filter(id_usuario_id=user_id).first()

    if carrito:
        items = ItemsCarrito.objects.filter(id_carrito=carrito)
        # Calcular el total sumando el subtotal de cada item
        total = sum(item.subtotal for item in items)  # Suma de subtotales
    else:
        items = []
        total = 0  # Total es 0 si no hay carrito

    context = {
        'items': items,
        'total': total,  # Pasar el total al contexto
    }

    return render(request, 'mi_carrito.html', context)


@role_required(allowed_roles=['Cliente'])
def eliminar_del_carrito(request):
    if request.method == "POST":
        items_a_eliminar = request.POST.getlist('items_a_eliminar')  # Obtiene una lista de IDs a eliminar
        if items_a_eliminar:
            # Elimina los items del carrito
            ItemsCarrito.objects.filter(id_itemsCarrito__in=items_a_eliminar).delete()
         
       

    return redirect('mi_carrito')  # Redirige de nuevo a la vista del carrito

# FIN Carrito

# INICIO Pedidos 
@role_required(allowed_roles=['Cliente'])
def realizar_pedido(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')

    # Obtener la dirección del usuario
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    direccion_entrega = usuario.direccion

    # Calcular el subtotal del carrito del cliente
    try:
        carrito = Carrito.objects.get(id_usuario=user_id)
        items = ItemsCarrito.objects.filter(id_carrito=carrito)
        subtotal = sum(item.subtotal for item in items)
    except Carrito.DoesNotExist:
        items = []  # Asegúrate de inicializar `items` en caso de que no haya carrito
        subtotal = 0

    context = {
        'direccion_entrega': direccion_entrega,
        'subtotal': subtotal,
        'items': items,  # Agregar los items al contexto
    }

    return render(request, 'view_realizarpedido.html', context)


@role_required(allowed_roles=['Cliente'])
def pedido_realizado(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        usuario = Usuario.objects.get(id_usuario=user_id)
        carrito = Carrito.objects.get(id_usuario=user_id)
        items = ItemsCarrito.objects.filter(id_carrito=carrito)
        
        if items.exists():
            # Crea el pedido
            pedido = Pedido.objects.create(
                fecha_pedido=timezone.now(),
                fecha_entrega=timezone.now() + timezone.timedelta(days=7),
                comentarios="Pedido realizado desde el carrito.",
                total=sum(item.subtotal for item in items),
                id_estado=EstadoPedido.objects.get(nombre_estado="Pendiente"),
                id_usuario=usuario
            )

            # Asociar los productos del carrito al pedido y limpiar el carrito
            for item in items:
                subtotal = item.cantidad * item.precio
                PedidoProducto.objects.create(
                    id_pedido=pedido,
                    id_producto=item.id_producto,
                    cantidad_producto=item.cantidad,
                    precio=item.precio,
                    subtotal=subtotal
                )

            items.delete()  # Limpia el carrito una vez que se ha creado el pedido
            carrito.delete()

            messages.success(request, "¡Pedido realizado exitosamente!")
            return redirect('pedido_exitoso',pedido_id = pedido.id_pedido)  # Redirige a la vista de éxito con el ID del pedido
        else:
            messages.error(request, "No hay productos en el carrito para realizar un pedido.")
        
    return redirect('mi_carrito')



@role_required(allowed_roles=['Cliente'])
def update_direccion(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        nueva_direccion = request.POST.get("direccion_entrega")
        if user_id and nueva_direccion:
            # Actualiza la dirección del usuario
            usuario = get_object_or_404(Usuario, id_usuario=user_id)
            usuario.direccion = nueva_direccion
            usuario.save()
            messages.success(request, "Dirección actualizada.")
        else:
            messages.error(request, "Error al actualizar la dirección.")

        return redirect('realizar_pedido')  # Asegúrate de redirigir a la vista correcta


@role_required(allowed_roles=['Cliente'])
def pedido_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    items = PedidoProducto.objects.filter(id_pedido=pedido)

    # Calcular el total sumando los subtotales de cada item
    total_pagar = sum(item.cantidad_producto * item.precio for item in items)  # Verifica que esto sea correcto

    context = {
        'pedido': pedido,
        'items': items,
        'total_pagar': total_pagar,  # Agregar el total al contexto
    }
    return render(request, 'v_pedidorealizado.html', context)

@role_required(allowed_roles=['Cliente'])
def enviar_comentario(request, pedido_id):
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id)

        # Actualizar el comentario del pedido
        if comentario:
            pedido.comentarios = comentario
            pedido.save()
            messages.success(request, "Comentario enviado exitosamente.")
        else:
            messages.warning(request, "El comentario no puede estar vacío.")

    return redirect('pedido_exitoso', pedido_id=pedido_id)


# FIN Pedidos 

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

def enviar_sugerencia(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        if request.session.get('user_role') == 'Cliente' and mensaje:
            sugerencia = Sugerencia(
                id_usuario_id=request.session['user_id'],
                mensaje=mensaje,
                fecha_envio=timezone.now()
            )
            sugerencia.save()
            messages.success(request, 'Sugerencia enviada con éxito')
        else:
            messages.error(request, 'No tienes permisos para enviar sugerencias')
    return redirect('cliente_view')


def logout_view(request):
    # Cerrar sesión en Django y también en Google
    auth_logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

# Vista para eliminar el producto
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado con éxito.')
    return redirect('ver_inventario') 