# Generated by Django 5.1.3 on 2024-12-04 22:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0004_remove_producto_imagen_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
