# Generated by Django 5.1 on 2024-09-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0007_alter_usuario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]