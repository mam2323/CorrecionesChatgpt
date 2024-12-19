from django.contrib import admin
from django.urls import path, include  # , re_path
# from django.views.generic import TemplateView
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

] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
