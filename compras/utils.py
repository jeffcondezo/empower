from maestro.models import CatalogoxProveedor


def save_detalleorden(detalle_orden):
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