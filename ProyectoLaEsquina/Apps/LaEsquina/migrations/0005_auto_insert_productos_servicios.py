from django.db import migrations

def create_initial_data(apps, schema_editor):
    # Obtener los modelos
    CategoriaProducto = apps.get_model('LaEsquina', 'CategoriaProducto')
    Producto = apps.get_model('LaEsquina', 'Producto')
    Servicio = apps.get_model('LaEsquina', 'Servicio')

    # Crear categorías de producto
    llantas_carro = CategoriaProducto.objects.create(nombre="Llantas para Carro")
    llantas_moto = CategoriaProducto.objects.create(nombre="Llantas para Moto")
    llantas_usadas = CategoriaProducto.objects.create(nombre="Llantas Usadas")
    lubricantes = CategoriaProducto.objects.create(nombre="Lubricantes")
    refrigerantes = CategoriaProducto.objects.create(nombre="Refrigerantes")
    accesorios = CategoriaProducto.objects.create(nombre="Accesorios de Reparación")

    # Insertar productos
    Producto.objects.bulk_create([
        Producto(nombre_producto="Llanta 205/55 R16", descripcion="Llanta para carro tamaño estándar", precio=80.00, id_categoria_producto=llantas_carro, cantidad_stock=10),
        Producto(nombre_producto="Llanta 120/70 ZR17", descripcion="Llanta para moto deportiva", precio=65.00, id_categoria_producto=llantas_moto, cantidad_stock=15),
        Producto(nombre_producto="Llanta usada 195/65 R15", descripcion="Llanta usada para carro en buen estado", precio=40.00, id_categoria_producto=llantas_usadas, cantidad_stock=5),
        Producto(nombre_producto="Lubricante 5W30", descripcion="Aceite sintético para motor", precio=10.00, id_categoria_producto=lubricantes, cantidad_stock=50),
        Producto(nombre_producto="Refrigerante Verde 1L", descripcion="Refrigerante verde para radiadores", precio=7.50, id_categoria_producto=refrigerantes, cantidad_stock=30),
        Producto(nombre_producto="Parche de reparación", descripcion="Accesorio para reparación de llantas", precio=2.00, id_categoria_producto=accesorios, cantidad_stock=100),
    ])

    # Insertar servicios
    Servicio.objects.bulk_create([
        Servicio(nombre_servicio="Armado de llantas", descripcion="Servicio de armado y desarmado de llantas", precio=15.00),
        Servicio(nombre_servicio="Aplicación de parches", descripcion="Reparación de llantas con parches", precio=8.00),
        Servicio(nombre_servicio="Revisión de llantas", descripcion="Chequeo completo de las llantas", precio=5.00),
        Servicio(nombre_servicio="Chequeo de la presión de llantas", descripcion="Medición y ajuste de presión de llantas", precio=3.00),
        Servicio(nombre_servicio="Colocación de centros", descripcion="Colocación de centros y tuercas", precio=12.00),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0004_insert_initial_roles_and_users'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
