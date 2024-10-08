# Generated by Django 5.1 on 2024-09-02 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id_carrito', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id_categoria_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id_estado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_servicio', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateField()),
                ('fecha_entrega', models.DateField()),
                ('comentarios', models.TextField(blank=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.estadopedido')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=100)),
                ('cantidad_stock', models.PositiveIntegerField()),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.categoriaproducto')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoProducto',
            fields=[
                ('id_pedido_producto', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_producto', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.pedido')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsCarrito',
            fields=[
                ('id_itemsCarrito', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.carrito')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.producto')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoServicio',
            fields=[
                ('id_pedido_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.pedido')),
                ('id_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudStock',
            fields=[
                ('id_solicitudStock', models.AutoField(primary_key=True, serialize=False)),
                ('plantilla', models.CharField(max_length=100)),
                ('fecha_solicitud', models.DateField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.producto')),
                ('id_proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.PositiveIntegerField()),
                ('direccion', models.CharField(max_length=255)),
                ('usuario', models.CharField(max_length=50, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.rol')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.usuario'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LaEsquina.usuario'),
        ),
    ]
