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
    # path('productos/', views.lista_productos,
    #      name='lista_productos'),  # Listar productos
    # path('producto/<int:producto_id>/', views.detalle_producto,
    #     name='detalle_producto'),  # Detalle producto
    # path('subir-imagen/<int:producto_id>/', views.subir_imagen,
    #    name='subir_imagen'),  # Subir imagen

    # Perfiles
    path('perfil/', views.perfil_view, name='perfil'),  # Vista del perfil
path('productos/', views.lista_productos, name='lista_productos'),

]
