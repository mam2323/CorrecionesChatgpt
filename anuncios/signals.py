from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

@receiver(post_save, sender=User)
def manejar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crear o guardar el perfil automáticamente cuando un usuario es creado o actualizado.
    """
    if created:
        Perfil.objects.create(user=instance)
    else:
        instance.perfil.save()
