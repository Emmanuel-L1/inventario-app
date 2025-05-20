from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductoForm
from inventario.models import Producto, Area
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


@login_required
def registrar_producto(request):
    perfil = getattr(request.user, 'perfil', None)

    if not perfil or not perfil.rol or perfil.rol.nombre.lower() != "encargado":
        return render(request, 'inventario/no_autorizado.html')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
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
    
    responsable_id = request.GET.get('responsable')
    query = request.GET.get('q') or ''

    edificio = request.GET.get('edificio')
    if edificio:
        productos = productos.filter(edificio=edificio)

    if responsable_id and responsable_id != '0':
        productos = productos.filter(responsable_id=responsable_id)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    responsables = User.objects.all()
    edificios = Producto.objects.values_list('edificio', flat=True).distinct()


    return render(request, 'inventario/lista_productos.html', {
    'productos': productos,
    'responsables': responsables,
    'selected_responsable': responsable_id,
    'query': query,
    'edificios': edificios,
    'selected_edificio': edificio,
})


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
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
    productos = Producto.objects.filter(is_active=True).order_by('nombre')

    edificio = request.GET.get('edificio') or ''
    responsable_id = request.GET.get('responsable') or ''
    query = request.GET.get('q') or ''

    if edificio:
        productos = productos.filter(edificio=edificio)

    if responsable_id and responsable_id != '0':
        productos = productos.filter(responsable_id=responsable_id)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    edificios = Producto.objects.values_list('edificio', flat=True).distinct()
    responsables = User.objects.all()

    paginator = Paginator(productos, 5)
    page_number = request.GET.get('page')
    productos_paginados = paginator.get_page(page_number)

    return render(request, 'inventario/lista_lectura.html', {
        'productos': productos_paginados,
        'edificios': edificios,
        'responsables': responsables,
        'selected_edificio': edificio,
        'selected_responsable': responsable_id,
        'query': query,
    })

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})

def generar_pdf_inventario(request):
    productos = Producto.objects.all()
    template_path = 'inventario/reporte.html'
    context = {'productos': productos}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF: %s' % pisa_status.err)
    return response