from django.db import models
from django.contrib.auth.models import User
from maestro.models import Proveedor, PresentacionxProducto, Producto, Almacen, TipoComprobante, Impuesto


# Create your models here.
# Total Final = > Total luego del descuento.
class Compra(models.Model):
    ESTADO_CHOICES = (
        ('1', 'GENERADO'),
        ('2', 'CONVERTIDO A PEDIDO'),
        ('3', 'COMPRA'),
        ('4', 'CANCELADO'),
        ('5', 'OCUPADO')
    )
    TIPO_CHOICES = (
        ('1', 'COMPRA DIRECTA'),
        ('2', 'PEDIDO'),
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=1)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default=1)
    is_financiado = models.BooleanField(default=False)
    is_entregado = models.BooleanField(default=False)
    fechahora_creacion = models.DateTimeField(auto_now_add=True)
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.PROTECT, null=True, blank=True)
    serie_comprobante = models.CharField(max_length=10, null=True, blank=True)
    numero_comprobante = models.CharField(max_length=10, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    impuesto_monto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion_pedido = models.IntegerField(blank=True, null=True)
    cantidad_presentacion_entrega = models.IntegerField(blank=True, null=True)
    cantidad_unidad_pedido = models.IntegerField(blank=True, null=True)
    cantidad_unidad_entrega = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    impuesto = models.ManyToManyField(Impuesto)
    impuesto_monto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_oferta = models.BooleanField(default=False)
    is_nodeseado = models.BooleanField(default=True)


class OfertaCompra(models.Model):
    TIPO_CHOICES = (
        (1, 'PRODUCTO'),
        (2, 'DESCUENTO MONETARIO'),
        (3, 'DESCUENTO PORCENTUAL'),
    )
    detallecompra = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    cantidad_compra = models.IntegerField()
    presentacion_compra = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                            related_name='presentacion_compra')
    retorno = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True)
    presentacion = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                     related_name='presentacion_oferta', blank=True, null=True)
