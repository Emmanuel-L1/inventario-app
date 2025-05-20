"""
URL configuration for INVENTARIOAPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path, include
from usuario.views import InicioSesionView
from django.contrib.auth.views import LogoutView
from usuario.views import inicio
from inventario.views import registrar_producto, lista_productos, editar_producto, eliminar_producto, vista_solo_lectura, detalle_producto, generar_pdf_inventario



urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('login/', InicioSesionView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('lectura/', vista_solo_lectura, name='vista_lectura'),
    path('productos/detalle/<int:producto_id>/', detalle_producto, name='detalle_producto'),
     path('reporte/inventario/', generar_pdf_inventario, name='reporte_inventario_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
