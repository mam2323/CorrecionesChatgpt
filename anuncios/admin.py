from .models import Room, Message
from django.contrib import admin
from .models import Categoria, Producto, Imagen, Perfil

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Imagen)
admin.site.register(Perfil)

admin.site.register(Room)
admin.site.register(Message)
