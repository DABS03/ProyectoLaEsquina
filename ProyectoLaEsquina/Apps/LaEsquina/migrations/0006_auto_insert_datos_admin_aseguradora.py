from django.db import migrations
from datetime import date

def create_admin_and_aseguradora_data(apps, schema_editor):
    Usuario = apps.get_model('LaEsquina', 'Usuario')
    Pedido = apps.get_model('LaEsquina', 'Pedido')
    EstadoPedido = apps.get_model('LaEsquina', 'EstadoPedido')
    Producto = apps.get_model('LaEsquina', 'Producto')
    Servicio = apps.get_model('LaEsquina', 'Servicio')
    PedidoProducto = apps.get_model('LaEsquina', 'PedidoProducto')
    PedidoServicio = apps.get_model('LaEsquina', 'PedidoServicio')

    # Crear estados de pedido
    estado_pendiente = EstadoPedido.objects.create(nombre_estado='Pendiente')
    estado_completado = EstadoPedido.objects.create(nombre_estado='Completado')

    # Obtener usuarios Cliente y Aseguradora
    cliente = Usuario.objects.get(usuario='cliente')
    aseguradora = Usuario.objects.get(usuario='aseguradora')

    # Crear pedidos
    Pedido.objects.bulk_create([
        Pedido(
            fecha_pedido=date(2024, 9, 10),
            fecha_entrega=date(2024, 9, 12),
            comentarios="Pedido urgente",
            total=120.00,
            id_estado=estado_pendiente,
            id_usuario=cliente
        ),
        Pedido(
            fecha_pedido=date(2024, 9, 15),
            fecha_entrega=date(2024, 9, 17),
            comentarios="Revisión general",
            total=30.00,
            id_estado=estado_pendiente,
            id_usuario=aseguradora
        ),
        Pedido(
            fecha_pedido=date(2024, 9, 20),
            fecha_entrega=date(2024, 9, 23),
            comentarios="Servicio regular",
            total=50.00,
            id_estado=estado_completado,
            id_usuario=cliente
        ),
    ])

    # Obtener productos y servicios
    producto_llanta = Producto.objects.get(nombre_producto="Llanta 205/55 R16")
    producto_lubricante = Producto.objects.get(nombre_producto="Lubricante 5W30")
    servicio_armado = Servicio.objects.get(nombre_servicio="Armado de llantas")
    servicio_revision = Servicio.objects.get(nombre_servicio="Revisión de llantas")

    # Crear pedidos de productos
    PedidoProducto.objects.bulk_create([
        PedidoProducto(
            id_pedido=Pedido.objects.get(fecha_pedido=date(2024, 9, 10)),
            id_producto=producto_llanta,
            cantidad_producto=2,
            precio=80.00,
            subtotal=160.00
        ),
        PedidoProducto(
            id_pedido=Pedido.objects.get(fecha_pedido=date(2024, 9, 20)),
            id_producto=producto_lubricante,
            cantidad_producto=3,
            precio=10.00,
            subtotal=30.00
        ),
    ])

    # Crear pedidos de servicios
    PedidoServicio.objects.bulk_create([
        PedidoServicio(
            id_pedido=Pedido.objects.get(fecha_pedido=date(2024, 9, 10)),
            id_servicio=servicio_armado,
            precio=15.00
        ),
        PedidoServicio(
            id_pedido=Pedido.objects.get(fecha_pedido=date(2024, 9, 15)),
            id_servicio=servicio_revision,
            precio=5.00
        ),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0005_auto_insert_productos_servicios'),
    ]

    operations = [
        migrations.RunPython(create_admin_and_aseguradora_data),
    ]
