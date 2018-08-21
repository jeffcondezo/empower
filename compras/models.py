from django.db import models
from django.contrib.auth.models import User
from maestro.models import Proveedor, PresentacionxProducto, Producto


# Create your models here.
class OrdenCompra(models.Model):
    ESTADO_CHOICES = (
        ('1', 'GENERADO'),
        ('2', 'CONVERTIDO A COMPRA'),
        ('3', 'CANCELADO')
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    compra = models.IntegerField(blank=True, null=True)
    total_tentativo = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class DetalleOrdenCompra(models.Model):
    ordencompra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion = models.IntegerField()
    cantidad_unidad = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2)


class Compra(models.Model):
    ESTADO_CHOICES = (
        ('1', 'RECIBIDO'),
        ('2', 'PAGADO'),
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado')
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    orden = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, related_name='orden_origen')
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion = models.IntegerField(blank=True, null=True)
    cantidad_unidad = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    is_oferta = models.BooleanField(default=False)


class OfertaOrden(models.Model):
    TIPO_CHOICES = (
        (1, 'PRODUCTO'),
        (2, 'DESCUENTO MONETARIO'),
        (3, 'DESCUENTO PORCENTUAL'),
    )
    detalleorden = models.ForeignKey(DetalleOrdenCompra, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    cantidad_compra = models.IntegerField()
    presentacion_compra = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                            related_name='presentacion_compra')
    retorno = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True)
    presentacion = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                     related_name='presentacion_oferta', blank=True, null=True)


class ResultadoOfertaOrden(models.Model):
    TIPO_CHOICES = (
        (1, 'PRODUCTO'),
        (2, 'DESCUENTO MONETARIO'),
        (3, 'DESCUENTO PORCENTUAL'),
    )
    detalleorden = models.ForeignKey(DetalleOrdenCompra, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True)
    presentacion = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT, blank=True, null=True)
    cantidad_presentacion = models.IntegerField(blank=True, null=True)
    cantidad_unidad = models.IntegerField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
