# Generated by Django 5.1.3 on 2024-12-10 20:40

import anuncios.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0009_alter_perfil_avatar_alter_perfil_bio_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(max_length=255, upload_to=anuncios.models.custom_upload_to),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.png', null=True, upload_to='avatars/'),
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorito_por', to='anuncios.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'producto')},
            },
        ),
    ]