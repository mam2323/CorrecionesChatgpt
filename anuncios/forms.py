from .models import Producto, Imagen
from django.utils.translation import gettext as _
from .models import Perfil
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'estado']


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email:",
        help_text=None  # Elimina el texto de ayuda predeterminado
    )
    password1 = forms.CharField(
        label="Contraseña:",
        widget=forms.PasswordInput,
        help_text=None  # Elimina el texto de ayuda predeterminado
    )
    password2 = forms.CharField(
        label="Confirmar contraseña:",
        widget=forms.PasswordInput,
        help_text=None  # Elimina el texto de ayuda predeterminado
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Usuario:",
        }
        help_texts = {
            "username": None,  # Elimina el texto de ayuda predeterminado
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar', 'bio', 'ubicacion']  # Campos editables
