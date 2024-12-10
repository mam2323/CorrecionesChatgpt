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
     path('favoritos/', views.ver_favoritos, name='favoritos'),
      path('favoritos/agregar/<int:producto_id>/', views.agregar_a_favoritos, name='agregar_favorito'),
    path('favoritos/eliminar/<int:producto_id>/', views.eliminar_de_favoritos, name='eliminar_favorito'),
]


