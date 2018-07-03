from django.db import models


class Empresa(models.Model):
    descripcion = models.CharField(max_length=150)
    ruc = models.CharField(max_length=11)


class Sucursal(models.Model):
    descripcion = models.CharField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=150)
    responsable = models.CharField(max_length=150)


class Categoria(models.Model):
    descripcion = models.CharField(max_length=250)
    nivel = models.SmallIntegerField()
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class Almacen(models.Model):
    descripcion = models.CharField(max_length=200)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)


class Producto(models.Model):
    descripcion = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)


class CatalogoProducto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)


class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)


class Kardex(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        (1, 'ENTRADA'),
        (2, 'SALIDA')
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=1, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_compra = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_venta = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)


class Presentacion(models.Model):
    descripcion = models.CharField(max_length=250)

