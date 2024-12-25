from django.db import models
from django.db.models import Max, Q, Prefetch
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Room, Message, Producto, Categoria, Favorito
from .forms import ProductoForm, PerfilForm, CustomUserCreationForm


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
def inbox(request):
    # Obtener todas las salas del usuario con mensajes prefetchados
    rooms = Room.objects.annotate(
        # Obtener el timestamp del último mensaje
        last_message_timestamp=Max('messages__timestamp')
    ).prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('timestamp'))
    ).filter(
        Q(user1=request.user) | Q(user2=request.user)
        # Ordenar por el último mensaje o la creación de la sala
    ).order_by('-last_message_timestamp', '-created_at')

    # Verificar si se está accediendo desde un dispositivo móvil
    is_mobile = request.GET.get('mobile', 'false') == 'true'

    # Determinar la sala activa si no es móvil o si se especifica un room_id
    room_id = request.GET.get('room_id')
    room = None
    if not is_mobile or room_id:
        room = get_object_or_404(Room, id=room_id) if room_id else (
            rooms.first() if rooms.exists() else None
        )

    # Mensajes de la sala activa
    messages = room.messages.all() if room else []

    return render(request, "anuncios/inbox.html", {
        "rooms": rooms,
        "room": room,
        "messages": messages,
        "product": room.product if room else None,
        "other_user": room.user2 if room and room.user1 == request.user else room.user1 if room else None,
        "is_mobile": is_mobile,
    })


@login_required
@csrf_exempt  # Permitir solicitudes sin CSRF si no estás usando un formulario estándar
def send_message(request, room_id):
    if request.method == 'POST':
        # Obtener el contenido del mensaje desde el formulario
        content = request.POST.get('content', '').strip()

        if content:
            # Buscar la sala por ID
            room = get_object_or_404(Room, id=room_id)

            # Crear y guardar el nuevo mensaje
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )

            # Devolver una respuesta exitosa con los datos del mensaje
            return JsonResponse({
                'status': 'success',
                'message': message.content,
                'timestamp': message.timestamp.strftime('%H:%M')
            })

    # Responder con error si algo falla
    return JsonResponse({'status': 'error', 'message': 'No se pudo enviar el mensaje'})


@login_required
def start_chat(request, product_id):
    # Obtener el producto por ID
    product = get_object_or_404(Producto, id=product_id)

    # Evitar que el usuario inicie un chat consigo mismo
    if product.usuario == request.user:
        return redirect('inbox')

    # Determinar los usuarios (el que inicia el chat y el propietario del producto)
    user1, user2 = sorted([request.user, product.usuario], key=lambda u: u.pk)

    # Crear o recuperar la sala de chat existente para este producto
    room, created = Room.objects.get_or_create(
        user1=user1,
        user2=user2,
        product=product,
    )

    # Redirigir al inbox con la sala activa
    return redirect(f"{reverse('inbox')}?room_id={room.id}")

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
