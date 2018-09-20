from django.db import models
from django.contrib.auth.models import User
from maestro.models import Proveedor, PresentacionxProducto, Producto, Almacen, TipoComprobante


# Create your models here.
# Total Final = > Total luego del descuento.
class OrdenCompra(models.Model):
    ESTADO_CHOICES = (
        ('1', 'GENERADO'),
        ('2', 'CONVERTIDO A PEDIDO'),
        ('3', 'CONVERTIDO A COMPRA'),
        ('4', 'CANCELADO')
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    compra = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2, default=0)


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
    ESTADO_ENVIO_CHOICES = (
        ('1', 'PEDIDO'),
        ('2', 'ENTREGADO'),
    )
    ESTADO_PAGO_CHOICES = (
        ('1', 'EN DEUDA'),
        ('2', 'PAGADO'),
    )
    TIPO_PAGO_CHOICES = (
        ('1', 'CONTADO'),
        ('2', 'CREDITO'),
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado')
    estado = models.CharField(max_length=1, choices=ESTADO_ENVIO_CHOICES, default=1)
    tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO_CHOICES, default=1)
    estado_pago = models.CharField(max_length=1, choices=ESTADO_PAGO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    orden = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, related_name='orden_origen')
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.PROTECT, null=True, blank=True)
    serie_comprobante = models.CharField(max_length=10, null=True, blank=True)
    numero_comprobante = models.CharField(max_length=10, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion_pedido = models.IntegerField(blank=True, null=True)
    cantidad_presentacion_entrega = models.IntegerField(blank=True, null=True)
    cantidad_unidad = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2)
    is_oferta = models.BooleanField(default=False)
    is_nodeseado = models.BooleanField(default=True)


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
