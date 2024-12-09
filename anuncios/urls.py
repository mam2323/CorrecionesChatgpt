from django.urls import path
from . import views


urlpatterns = [
    # Página principal
    path('', views.home, name='home'),  # Página principal de la app

    # Usuarios
    path('registro/', views.registro, name='registro'),  # Registro tradicional

    # Productos
    path('publicar/', views.publicar_producto,
         name='publicar_producto'),  # Publicar producto

    # Perfiles
    path('perfil/', views.perfil_view, name='perfil'),  # Vista del perfil
path('productos/', views.lista_productos, name='lista_productos'),
    path('editar_anuncio/<int:anuncio_id>/', views.editar_anuncio, name='editar_anuncio'),

]
