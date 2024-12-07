from django.db import models
from django.contrib.auth.models import User

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
            ('España', 'España')  # Solo estas opciones estarán disponibles
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
    fecha_publicacion = models.DateTimeField(
        auto_now_add=True
    )  # Campo de fecha

    def __str__(self):
        return self.titulo

# Tabla para múltiples imágenes asociadas a un producto


class Imagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.titulo}"

# Tabla de Chats


class Chat(models.Model):
    usuarios = models.ManyToManyField(User)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"

# Tabla de Mensajes


class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.chat.id}"


# Tabla de Perfiles


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, default='avatars/default-avatar.png')
    bio = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)
