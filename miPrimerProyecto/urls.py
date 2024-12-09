from django.contrib import admin
from django.urls import path, include  # Importa include para incluir las URLs de las apps
from django.contrib.auth import views as auth_views  # Para vistas genéricas de autenticación
from django.conf import settings
from django.conf.urls.static import static  # Para servir archivos estáticos y multimedia

urlpatterns = [
    # Administración de Django
    path('admin/', admin.site.urls),

    # URLs de la app 'anuncios' (página principal y funcionalidades relacionadas)
    path('', include('anuncios.urls')),  # Incluye las URLs de la app 'anuncios'

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='account_login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'), name='logout'),  # Logout (redirige al home después de salir)
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
