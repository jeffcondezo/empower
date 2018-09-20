from almacen.models import Kardex, Stock
from maestro.models import Almacen
import json


def update_kardex_stock(detalle, tipo_movimiento, tipo_detalle):
    almacen = Almacen.objects.get(pk=1)
    try:
        stock = Stock.objects.get(producto=detalle.producto_id, almacen=almacen.id)
    except Stock.DoesNotExist:
        stock = Stock(producto=detalle.producto, almacen=almacen)
    stock.cantidad = stock.cantidad + detalle.cantidad_unidad
    stock.save()
    kardex = Kardex(almacen=almacen, producto=detalle.producto, tipo_movimiento=tipo_movimiento,
                    tipo_detalle=tipo_detalle, cantidad=detalle.cantidad_unidad, id_target=detalle.id)
    if tipo_movimiento == 1:
        kardex.cantidad_entrada = kardex.cantidad
        kardex.precio_unitario_entrada = detalle.precio
    else:
        kardex.cantidad_salida = kardex.cantidad
        kardex.precio_unitario_salida = detalle.precio
    kardex.save()

