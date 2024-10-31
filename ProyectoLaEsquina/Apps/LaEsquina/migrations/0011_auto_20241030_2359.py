from django.db import migrations

def eliminar_estados(apps, schema_editor):
    EstadoPedido = apps.get_model('LaEsquina', 'EstadoPedido')
    EstadoPedido.objects.filter(id_estado=3).delete()
    EstadoPedido.objects.filter(id_estado=5).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0010_alter_producto_imagen'),  # Reemplaza con el nombre de la última migración existente
    ]

    operations = [
        migrations.RunPython(eliminar_estados),
    ]
