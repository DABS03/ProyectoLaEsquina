from django.db import migrations

def create_roles_and_users(apps, schema_editor):
    Rol = apps.get_model('LaEsquina', 'Rol')
    Usuario = apps.get_model('LaEsquina', 'Usuario')

    # Crear roles
    admin_rol = Rol.objects.create(nombre_rol='Admin')
    cliente_rol = Rol.objects.create(nombre_rol='Cliente')
    aseguradora_rol = Rol.objects.create(nombre_rol='Aseguradora')

    # Crear usuarios
    Usuario.objects.create(nombres='Admin', correo='admin@laesquina.com', telefono=123456789, 
                           direccion='Calle Falsa 123', usuario='admin', contrasena='admin123', id_rol=admin_rol)
    
    Usuario.objects.create(nombres='Cliente', correo='cliente@laesquina.com', telefono=987654321, 
                           direccion='Calle Real 456', usuario='cliente', contrasena='cliente123', id_rol=cliente_rol)
    
    Usuario.objects.create(nombres='Aseguradora', correo='aseguradora@laesquina.com', telefono=192837465, 
                           direccion='Avenida Principal 789', usuario='aseguradora', contrasena='aseguradora123', id_rol=aseguradora_rol)

class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0003_auto_20240902_0018'),  
    ]

    operations = [
        migrations.RunPython(create_roles_and_users),
    ]
