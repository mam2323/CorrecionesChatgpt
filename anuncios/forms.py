from .models import Perfil
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Imagen


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
        required=True, help_text="Requerido. Introduce un email válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar', 'bio', 'ubicacion']  # Campos editables
