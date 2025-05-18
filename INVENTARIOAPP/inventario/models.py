from django.contrib.auth.models import User
from django.db import models

class ProductoManager(models.Manager):
    def activos(self):
        return super().get_queryset().filter(is_active=True)
class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    año = models.PositiveIntegerField()
    numero_inventario = models.CharField(max_length=50, unique=True)
    edificio = models.CharField(max_length=100)
    aula = models.CharField(max_length=100)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    objects = ProductoManager()

    def __str__(self):
        return f"{self.nombre} ({self.numero_inventario})"

