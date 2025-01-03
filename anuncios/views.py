from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductoForm, PerfilForm
from .models import Producto, Categoria


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
    # Obtener el perfil del usuario actual
    perfil = request.user.perfil
    if request.method == 'POST':
        # Si se envía un formulario, procesa los datos del perfil
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Tu perfil ha sido actualizado correctamente.')
            # Redirige a la misma página después de guardar
            return redirect('perfil')
    else:
        # Carga el formulario con los datos actuales del perfil
        form = PerfilForm(instance=perfil)

    # Renderiza la plantilla del perfil con el formulario
    return render(request, 'anuncios/perfil.html', {'perfil': perfil, 'form': form})


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


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige al login tras el registro
            return redirect('account_login')
    else:
        form = UserCreationForm()
    return render(request, 'anuncios/registro.html', {'form': form})
