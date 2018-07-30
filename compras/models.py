from django.db import models
from django.contrib.auth.models import User
from maestro.models import Proveedor, PresentacionxProducto


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
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion_pedido = models.IntegerField()
    cantidad_pedido = models.IntegerField()
    precio_tentativo = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class Compra(models.Model):
    ESTADO_CHOICES = (
        (1, 'PEDIDO'),
        (2, 'ENTREGADO'),
        (3, 'CANCELADO'),
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado')
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    orden = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, related_name='orden_origen')
    fecha_idealentrega = models.DateField()
    fechahora_entrega = models.DateTimeField()
    is_conforme = models.BooleanField()
    recepcionista = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recepcionista')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=8, decimal_places=2)
    precio_sindescuento = models.DecimalField(max_digits=8, decimal_places=2)


class DetalleCompra(models.Model):
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion_entrega = models.IntegerField(blank=True, null=True)
    cantidad_entrega = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    cantidad_presentacion_diferencia = models.IntegerField(blank=True, null=True)
    cantidad_diferencia = models.IntegerField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2)
    precio_sindescuento = models.DecimalField(max_digits=8, decimal_places=2)
    is_genoferta = models.BooleanField(default=False)
    is_oferta = models.BooleanField(default=False)


class OfertaCompra(models.Model):
    ESTADO_CHOICES = (
        (1, 'PRODUCTO'),
        (2, 'DESCUENTO UNICO'),
        (3, 'DESCUENTO GRADUAL'),
    )
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
