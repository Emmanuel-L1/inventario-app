from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductoForm
from inventario.models import Producto, Area
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def registrar_producto(request):
    perfil = getattr(request.user, 'perfil', None)

    if not perfil or not perfil.rol or perfil.rol.nombre.lower() != "encargado":
        return render(request, 'inventario/no_autorizado.html')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.responsable = request.user
            producto.save()
            return redirect('inicio')
    else:
        form = ProductoForm()

    return render(request, 'inventario/registro_producto.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()

    # Obtener parámetros del filtro
    area_id = request.GET.get('area')
    responsable_id = request.GET.get('responsable')
    query = request.GET.get('q')

    if area_id and area_id != '0':
        productos = productos.filter(area_id=area_id)

    if responsable_id and responsable_id != '0':
        productos = productos.filter(responsable_id=responsable_id)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    areas = Area.objects.all()
    responsables = User.objects.all()

    return render(request, 'inventario/lista_productos.html', {
        'productos': productos,
        'areas': areas,
        'responsables': responsables,
        'selected_area': area_id,
        'selected_responsable': responsable_id,
        'query': query,
    })

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('lista_productos')
    return render(request, 'inventario/registro_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect('lista_productos')
    return render(request, 'inventario/confirmar_eliminacion.html', {'producto': producto})

@login_required
def vista_solo_lectura(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol.nombre if perfil and perfil.rol else None

    if rol not in ['Invitado', 'Responsable de área', 'Encargado']:
        return render(request, 'inventario/no_autorizado.html')

    productos = Producto.objects.all()

    area_id = request.GET.get('area')
    responsable_id = request.GET.get('responsable')
    query = request.GET.get('q')

    if area_id and area_id != '0':
        productos = productos.filter(area_id=area_id)
    if responsable_id and responsable_id != '0':
        productos = productos.filter(responsable_id=responsable_id)
    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))

    paginator = Paginator(productos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    areas = Area.objects.all()
    responsables = User.objects.all()

    return render(request, 'inventario/lista_lectura.html', {
        'page_obj': page_obj,
        'areas': areas,
        'responsables': responsables,
        'selected_area': area_id,
        'selected_responsable': responsable_id,
        'query': query,
    })

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})