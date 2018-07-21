from django.db import models
from maestro.models import Producto, Almacen


# Create your models here.
class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)


class Kardex(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        (1, 'ENTRADA'),
        (2, 'SALIDA')
    )
    TIPO_DETALLE_CHOICES = (
        (1, 'COMPRA'),
        (2, 'VENTA')
    )
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=1, choices=TIPO_MOVIMIENTO_CHOICES)
    tipo_detalle = models.CharField(max_length=1, choices=TIPO_DETALLE_CHOICES)
    cantidad = models.IntegerField()
    cantidad_entrada = models.IntegerField(blank=True, null=True)
    cantidad_salida = models.IntegerField(blank=True, null=True)
    id_target = models.IntegerField()
    fechahora = models.DateTimeField()
