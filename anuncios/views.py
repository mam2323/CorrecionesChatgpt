from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ProductoForm, PerfilForm, CustomUserCreationForm
from .models import Producto, Categoria, Favorito

# Vista: Home con filtros


@login_required
def home(request):
    query = request.GET.get('q', '')
    ubicacion = request.GET.get('ubicacion', '')
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    orden = request.GET.get('orden', '')

    productos = Producto.objects.prefetch_related(
        'imagenes').select_related('usuario__perfil')

    if query:
        productos = productos.filter(titulo__icontains=query)
    if ubicacion:
        productos = productos.filter(ubicacion=ubicacion)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if estado:
        productos = productos.filter(estado=estado)

    if orden == "precio_asc":
        productos = productos.order_by('precio', '-fecha_publicacion')
    elif orden == "precio_desc":
        productos = productos.order_by('-precio', '-fecha_publicacion')
    else:
        productos = productos.order_by('-fecha_publicacion')

    categorias = Categoria.objects.all()
    favoritos = Favorito.objects.filter(
        usuario=request.user).values_list('producto_id', flat=True)

    context = {
        'productos': productos,
        'query': query,
        'ubicacion': ubicacion,
        'categoria_id': categoria_id,
        'estado': estado,
        'orden': orden,
        'categorias': categorias,
        'favoritos': favoritos,
    }
    return render(request, 'home.html', context)

# Vista: Perfil del usuario


@login_required
def perfil_view(request):
    perfil = request.user.perfil
    anuncios = Producto.objects.filter(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'anuncios/perfil.html', {
        'perfil': perfil,
        'form': form,
        'anuncios': anuncios
    })

# Vista: Publicar producto


@login_required
def publicar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()

            for imagen in request.FILES.getlist('imagenes'):
                producto.imagenes.create(imagen=imagen)

            messages.success(request, 'Producto publicado exitosamente.')
            return redirect('home')
    else:
        form = ProductoForm()
    return render(request, 'anuncios/publicar_producto.html', {'form': form})

# Vista: Registro de usuarios


def registro(request):
    next_url = request.GET.get('next', 'perfil')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Vista: Lista de productos


@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'anuncios/lista_productos.html', {'productos': productos})

# Vista: Editar anuncio


@login_required
def editar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Producto, id=anuncio_id, usuario=request.user)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'El anuncio se ha actualizado correctamente.')
            return redirect('perfil')
    else:
        form = ProductoForm(instance=anuncio)

    return render(request, 'anuncios/editar_anuncio.html', {'form': form, 'anuncio': anuncio})

# Vista: Ver favoritos


@login_required
def ver_favoritos(request):
    favoritos = Favorito.objects.filter(
        usuario=request.user).select_related('producto')
    return render(request, 'anuncios/favoritos.html', {'favoritos': favoritos})

# Vista: Agregar a favoritos


@login_required
def agregar_a_favoritos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    favorito, created = Favorito.objects.get_or_create(
        usuario=request.user, producto=producto)
    return JsonResponse({'status': 'added' if created else 'exists', 'producto_id': producto_id})


@login_required
def chat_index(request):
    return render(request, "anuncios/chat.html", {"room_name": "default"})


@login_required
def room(request, room_name):
    return render(request, "anuncios/chat.html", {"room_name": room_name})

# Vista: Eliminar de favoritos


@login_required
def eliminar_de_favoritos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    favorito = Favorito.objects.filter(
        usuario=request.user, producto=producto).first()
    if favorito:
        favorito.delete()
        return JsonResponse({'status': 'removed', 'producto_id': producto_id})
    return JsonResponse({'status': 'not_found', 'producto_id': producto_id})
