from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Responsable(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    año = models.PositiveIntegerField()
    numero_inventario = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_inventario})"
