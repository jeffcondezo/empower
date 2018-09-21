from django.db import models
from maestro.models import Sucursal, TipoComprobante, Producto, PresentacionxProducto
from clientes.models import Cliente


# Create your models here.
class Venta(models.Model):
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
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_ENVIO_CHOICES, default=1)
    tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO_CHOICES, default=1)
    estado_pago = models.CharField(max_length=1, choices=ESTADO_PAGO_CHOICES, default=1)
    fechahora = models.DateTimeField(auto_now_add=True)
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.PROTECT, null=True, blank=True)
    serie_comprobante = models.CharField(max_length=10, null=True, blank=True)
    numero_comprobante = models.CharField(max_length=10, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
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


class OfertaVenta(models.Model):
    TIPO_DURACION_CHOICES = (
        (1, 'TEMPORAL'),
        (2, 'PERMANENTE'),
    )
    TIPO_CHOICES = (
        (1, 'PRODUCTO'),
        (2, 'DESCUENTO MONETARIO'),
        (3, 'DESCUENTO PORCENTUAL'),
    )
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    tipo_duracion = models.CharField(max_length=1, choices=TIPO_DURACION_CHOICES)
    producto_oferta = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto_oferta_venta')
    presentacion_oferta = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                            related_name='presentacion_oferta_venta')
    cantidad_oferta = models.IntegerField()
    producto_retorno = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='producto_retorno_venta')
    presentacion_retorno = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                             related_name='presentacion_retorno_venta', blank=True, null=True)
    retorno = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fechahora_inicio = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fechahora_fin = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    stock_limite = models.DateTimeField(auto_now_add=True, blank=True, null=True)
