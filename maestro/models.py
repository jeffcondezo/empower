from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    descripcion = models.CharField(max_length=150)
    ruc = models.CharField(max_length=11)

    def __str__(self):
        return self.descripcion


class Sucursal(models.Model):
    descripcion = models.CharField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=150)
    responsable = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion


class Categoria(models.Model):
    descripcion = models.CharField(max_length=250)
    nivel = models.SmallIntegerField()
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    padre_total = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='padretotal')

    def __str__(self):
        return self.descripcion


class Almacen(models.Model):
    descripcion = models.CharField(max_length=200)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)


class Producto(models.Model):
    descripcion = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)
    catalogo = models.ManyToManyField(Sucursal)


class Presentacion(models.Model):
    descripcion = models.CharField(max_length=250)
    # Agregar abreviatura


class PresentacionxProducto(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()


class Proveedor(models.Model):
    descripcion = models.CharField(max_length=250)
    ruc = models.CharField(max_length=11)


class CatalogoxProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio_tentativo = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class PrecioxProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    fechahora = models.DateTimeField()


class Modulo(models.Model):
    descripcion = models.CharField(max_length=250)


class Vista(models.Model):
    descripcion = models.CharField(max_length=250)
    modulo = models.ForeignKey(Modulo, on_delete=models.PROTECT)


class Accion(models.Model):
    descripcion = models.CharField(max_length=250)


class AccionxVista(models.Model):
    accion = models.ForeignKey(Accion, on_delete=models.PROTECT)
    vista = models.ForeignKey(Vista,on_delete=models.PROTECT)


class AsignacionAccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accionxvista = models.ForeignKey(AccionxVista, on_delete=models.PROTECT)


