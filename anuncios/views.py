from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductoForm, PerfilForm
from .models import Producto, Categoria
 
def home(request):
    # Filtros
    query = request.GET.get('q', '')
    ubicacion = request.GET.get('ubicacion', '')
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    orden = request.GET.get('orden', '')

    # Productos con relaciones prefetch
    productos = Producto.objects.prefetch_related('imagenes').select_related('usuario__perfil')

    # Aplicar filtros opcionales
    if query:
        productos = productos.filter(titulo__icontains=query)
    if ubicacion:
        productos = productos.filter(ubicacion=ubicacion)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if estado:
        productos = productos.filter(estado=estado)

    # Ordenar productos
    if orden == "precio_asc":
        productos = productos.order_by('precio', '-fecha_publicacion')
    elif orden == "precio_desc":
        productos = productos.order_by('-precio', '-fecha_publicacion')
    else:
        productos = productos.order_by('-fecha_publicacion')

    # Categorías
    categorias = Categoria.objects.all()

    # Contexto
    context = {
        'productos': productos,
        'query': query,
        'ubicacion': ubicacion,
        'categoria_id': categoria_id,
        'estado': estado,
        'orden': orden,
        'categorias': categorias,
    }

    return render(request, 'home.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PerfilForm
from .models import Producto

@login_required
def perfil_view(request):
    perfil = request.user.perfil
    anuncios = Producto.objects.filter(usuario=request.user)  # Anuncios del usuario

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'anuncios/perfil.html', {
        'perfil': perfil,
        'form': form,
        'anuncios': anuncios  # Pasar anuncios al template
    })


from django.contrib.auth.decorators import login_required
@login_required
def publicar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()

            # Guardar imágenes múltiples si es necesario
            for imagen in request.FILES.getlist('imagenes'):
                producto.imagenes.create(imagen=imagen)

            messages.success(request, 'Producto publicado exitosamente.')
            return redirect('home')  # Redirige al home tras publicar
    else:
        form = ProductoForm()
    return render(request, 'anuncios/publicar_producto.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Importa tu formulario personalizado

def registro(request):
    next_url = request.GET.get('next', 'perfil')  # Redirige al perfil por defecto
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()  # Crea el usuario
            login(request, user)  # Inicia sesión automáticamente tras el registro
            return redirect(next_url)  # Redirige a la URL original o al perfil
    else:
        form = CustomUserCreationForm()  # Carga el formulario vacío
    return render(request, 'registration/register.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'anuncios/lista_productos.html', {'productos': productos})


@login_required
def editar_anuncio(request, anuncio_id):
    anuncio = Producto.objects.get(id=anuncio_id, usuario=request.user)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            messages.success(request, 'El anuncio se ha actualizado correctamente.')
            return redirect('perfil')
    else:
        form = ProductoForm(instance=anuncio)

    return render(request, 'anuncios/editar_anuncio.html', {'form': form, 'anuncio': anuncio})
