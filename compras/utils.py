from maestro.models import CatalogoxProveedor
from compras.models import DetalleOrdenCompra


def fill_data(detalle_orden):
    presentacionxproducto = detalle_orden.presentacionxproducto
    cantidad_conversion = presentacionxproducto.cantidad
    cantidad_presentacion = detalle_orden.cantidad_presentacion_pedido
    detalle_orden.cantidad_pedido = cantidad_conversion * cantidad_presentacion
    try:
        catalogo_proveedor = CatalogoxProveedor.objects.get(presentacionxproducto=presentacionxproducto.id)
        detalle_orden.precio_tentativo = catalogo_proveedor.precio_tentativo
        detalle_orden.total = catalogo_proveedor.precio_tentativo * cantidad_presentacion
    except CatalogoxProveedor.DoesNotExist:
        detalle_orden.precio_tentativo = 0
        detalle_orden.total = 0
    detalle_orden.save()


def recalcular_total_orden(orden):
    detalleorden = DetalleOrdenCompra.objects.filter(ordencompra=orden.id)
    total = 0
    for d in detalleorden:
        total += d.total
    orden.total_tentativo = total
    orden.save()

