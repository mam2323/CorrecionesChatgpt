from django.contrib import admin
from django.urls import path, include  # Importa include
from django.contrib.auth import views as auth_views  # Agrega esta línea
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluye las rutas de la app 'anuncios'
    path('', include('anuncios.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
