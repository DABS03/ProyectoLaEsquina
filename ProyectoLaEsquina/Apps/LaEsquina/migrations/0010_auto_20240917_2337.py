from django.db import migrations
from django.core.files import File
import os

def load_images(apps, schema_editor):
    Producto = apps.get_model('LaEsquina', 'Producto')
    media_root = 'media/productos/'  # Ruta relativa a la carpeta de medios

    imagenes = {
        'Llanta 20555 R16.jpg': 'Llanta 205/55 R16',
        'Llanta 12070 ZR17.jpg': 'Llanta 120/70 ZR17',
        'Llanta usada 19565 R15.jpg': 'Llanta usada 195/65 R15',
        'Lubricante 5W30.jpg': 'Lubricante 5W30',
        'Refrigerante Verde 1L.jpg': 'Refrigerante Verde 1L',
        'Parche de reparación.jpg': 'Parche de reparación',
    }

    for nombre_archivo, nombre_producto in imagenes.items():
        ruta_imagen = os.path.join(media_root, nombre_archivo)
        if os.path.exists(ruta_imagen):
            with open(ruta_imagen, 'rb') as imagen:
                try:
                    producto = Producto.objects.get(nombre_producto=nombre_producto)
                    if producto:
                        producto.imagen.save(nombre_archivo, File(imagen))
                        print(f"Imagen '{nombre_archivo}' cargada para el producto '{nombre_producto}'.")
                    else:
                        print(f"Producto '{nombre_producto}' no encontrado. Verifica el nombre en la base de datos.")
                except Producto.DoesNotExist:
                    print(f"Producto '{nombre_producto}' no encontrado en la base de datos. Verifica el nombre.")
        else:
            print(f"Archivo de imagen '{nombre_archivo}' no encontrado en '{ruta_imagen}'.")

class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0009_remove_usuario_imagen'),
    ]

    operations = [
        migrations.RunPython(load_images),
    ]
