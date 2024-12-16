from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Administración de Django
    path('admin/', admin.site.urls),

    # URLs de la app 'anuncios' (página principal y funcionalidades relacionadas)
    path('', include('anuncios.urls')),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='account_login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'), name='logout'),  # Logout

    # Para React (frontend)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='react'),
]

# Servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
