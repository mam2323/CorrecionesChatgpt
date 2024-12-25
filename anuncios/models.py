import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Asegúrate de que Producto está correctamente importado


# Función para renombrar archivos al subirlos
def custom_upload_to(instance, filename):
    # Truncar el nombre del archivo y mantener la extensión
    base, ext = os.path.splitext(filename)
    # Limitar el nombre a 50 caracteres y eliminar caracteres especiales
    base = slugify(base[:50])
    return f"productos/{base}{ext}"


# Tabla de Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# Tabla de Productos
class Producto(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ubicacion = models.CharField(
        max_length=200,
        choices=[
            ('Campamentos Saharauis', 'Campamentos Saharauis'),
            ('Tindouf', 'Tindouf'),
            ('Mauritania', 'Mauritania'),
            ('España', 'España')
        ],
        blank=True,
        null=True
    )
    estado = models.CharField(
        max_length=15,
        choices=[
            ('Nuevo', 'Nuevo'),
            ('Segunda mano', 'Segunda mano')
        ],
        default='Nuevo'
    )
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# Tabla para múltiples imágenes asociadas a un producto
class Imagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='imagenes'
    )
    imagen = models.ImageField(upload_to=custom_upload_to, max_length=255)

    def __str__(self):
        return f"Imagen de {self.producto.titulo}"


# Tabla de Perfiles
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png'
    )
    bio = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Tabla de Favoritos
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un usuario no puede agregar el mismo producto varias veces
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.titulo}"


class Room(models.Model):
    user1 = models.ForeignKey(
        User, related_name='room_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='room_user2', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'anuncios.Producto', on_delete=models.CASCADE)  # Referencia por cadena
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat sobre {self.product.titulo} entre {self.user1.username} y {self.user2.username}"


class Message(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
