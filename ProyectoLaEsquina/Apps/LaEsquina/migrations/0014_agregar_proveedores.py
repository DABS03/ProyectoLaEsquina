from django.db import migrations

def agregar_proveedores(apps, schema_editor):
    Proveedor = apps.get_model('LaEsquina', 'Proveedor')
    Proveedor.objects.create(nombre_proveedor="Proveedor 1", correo="diego.burgos@catolica.edu.sv")
    Proveedor.objects.create(nombre_proveedor="Proveedor 2", correo="d.a.burgos.servellon@gmail.com")

class Migration(migrations.Migration):
    dependencies = [
        ('LaEsquina', '0013_pedidoservicio_direccion_servicio_and_more'),
    ]

    operations = [
        migrations.RunPython(agregar_proveedores),
    ]
