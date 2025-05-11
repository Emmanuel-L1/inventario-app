from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductoForm

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
