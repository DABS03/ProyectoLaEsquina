from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaEsquina', '0009_remove_usuario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]