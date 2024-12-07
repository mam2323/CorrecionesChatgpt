# Importar formulario predeterminado de registro
from django.contrib import messages
from .forms import ProductoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PerfilForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Producto, Categoria  # Importar los modelos necesarios


def home(request):
    # Obtener parámetros de búsqueda y filtros desde la URL
    query = request.GET.get('q', '')  # Texto de búsqueda
    ubicacion = request.GET.get('ubicacion', '')  # Filtro por ubicación
    categoria_id = request.GET.get('categoria', '')  # Filtro por categoría
    estado = request.GET.get('estado', '')  # Filtro por estado
    orden = request.GET.get('orden', '')  # Filtro de orden

    # Obtener todos los productos inicialmente
    productos = Producto.objects.prefetch_related('imagenes').all()

    # Aplicar filtros opcionales
    if query:
        productos = productos.filter(titulo__icontains=query)
    if ubicacion:
        productos = productos.filter(ubicacion=ubicacion)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if estado:
        productos = productos.filter(estado=estado)

    # Aplicar orden
    if orden == "precio_asc":
        productos = productos.order_by('precio')
    elif orden == "precio_desc":
        productos = productos.order_by('-precio')
    elif orden == "reciente":
        productos = productos.order_by('-fecha_publicacion')

    # Obtener todas las categorías para mostrarlas en el filtro
    categorias = Categoria.objects.all()

    # Contexto para la plantilla
    context = {
        'productos': productos,  # Lista de productos filtrados
        'query': query,  # Texto de búsqueda actual
        'ubicacion': ubicacion,  # Ubicación seleccionada
        'categoria_id': categoria_id,  # Categoría seleccionada
        'estado': estado,  # Estado seleccionado
        'orden': orden,  # Orden seleccionado
        'categorias': categorias,  # Todas las categorías disponibles
    }

    # Renderizar la plantilla
    return render(request, 'home.html', context)


@login_required
def perfil_view(request):
    try:
        perfil = request.user.perfil
        # Si el perfil existe, renderiza la plantilla del perfil
        return render(request, 'anuncios/perfil.html', {'perfil': perfil})
    except AttributeError:
        # Si el perfil no existe, muestra un mensaje o redirige
        messages.error(
            request, 'Debes completar tu perfil antes de acceder a esta página.')
        # Redirige a la página de login o registro
        return redirect('account_login')


@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige a la vista del perfil
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'anuncios/editar_perfil.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autentica al usuario automáticamente tras registrarlo
            login(request, user)
            return redirect('home')  # Redirige a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def publicar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user  # Asigna el usuario actual como propietario
            producto.save()
            # Redirige a la lista de productos
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'anuncios/publicar_producto.html', {'form': form})
