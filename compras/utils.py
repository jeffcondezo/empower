from maestro.models import CatalogoxProveedor, Producto, PresentacionxProducto
from compras.models import DetalleOrdenCompra, DetalleCompra, OfertaCompra
import json


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


def crear_detallecompra(detalle_orden, request, compra):
    for idx, d in enumerate(detalle_orden, start=1):
        precio = float(request['precio-'+str(idx)])
        detallecompra = DetalleCompra(compra=compra, producto=d.producto,
                                      presentacionxproducto=d.presentacionxproducto,
                                      cantidad_presentacion_entrega=d.cantidad_presentacion_pedido,
                                      cantidad_entrega=d.cantidad_pedido, precio_sindescuento=precio)
        oferta = request['oferta-'+str(idx)]
        if oferta != '':
            detallecompra.is_genoferta = True
            oferta = json.loads(request['oferta-'+str(idx)])
            for o in oferta:
                validar = validar_oferta(o)
                if validar[0]:
                    aplicar_oferta(o, detallecompra, validar)
        else:
            detallecompra.precio = detallecompra.precio_sindescuento
            detallecompra.descuento = 0
            detallecompra.save()


def validar_oferta(oferta):
    is_valid = False
    retorno = []
    if oferta[0] not in ['1', '2', '3']:
        return [is_valid]
    if not int(oferta[1]) > 0:
        return [is_valid]
    if not float(oferta[2]) > 0:
        return [is_valid]
    if len(oferta) > 3:
        try:
            producto = Producto.objects.get(pk=oferta[3])
            presentacion = PresentacionxProducto.objects.get(pk=oferta[4])
        except (Producto.DoesNotExist, PresentacionxProducto.DoesNotExist) as e:
            return [is_valid]
        is_valid = True
        retorno.extend([is_valid, producto, presentacion])
    else:
        return [True]


def aplicar_oferta(oferta, detallecompra, validar):
    oferta_compra = OfertaCompra(detallecompra=detallecompra, tipo=oferta[0], cantidad_compra=oferta[1],
                                 presentacion_compra=detallecompra.presentacionxproducto, retorno=oferta[2])
    if len(oferta) > 3:
        oferta_compra.producto_oferta = validar[1]
        oferta_compra.presentacion_oferta = validar[2]
        if oferta[1] == '2':
            cantidad_comprada = detallecompra.cantidad_entrega
            cantidad_oferta = int(oferta[1])
            retorno = float(oferta[2])
            detallecompra.descuento = (cantidad_comprada // cantidad_oferta)*retorno
            detallecompra.precio = detallecompra.precio_sindescuento - detallecompra.descuento
            detallecompra.save()
        elif oferta[1] == '3':
            if detallecompra.cantidad_entrega > int(oferta[1]):
                detallecompra.descuento = 100 * float(oferta[2])/detallecompra.precio_sindescuento
            else:
                detallecompra.descuento = 0
            detallecompra.precio = detallecompra.precio_sindescuento - detallecompra.descuento
            detallecompra.save()
    else:
        if detallecompra.cantidad_entrega > int(oferta[1]):
            producto_oferta = Producto.objects.get(pk=oferta[3])
            presentacion_oferta = PresentacionxProducto.objects.get(pk=oferta[4])
            cantidad_comprada = detallecompra.cantidad_entrega
            cantidad_oferta = int(oferta[1])
            retorno = int(oferta[2])
            cantidad_regalo = (cantidad_comprada // cantidad_oferta) * retorno
            detallecompra_oferta = DetalleCompra(compra=detallecompra.compra, producto=producto_oferta,
                                                 presentacionxproducto=presentacion_oferta,
                                                 cantidad_presentacion_entrega=cantidad_regalo,
                                                 cantidad_entrega=cantidad_oferta*presentacion_oferta.cantidad,
                                                 precio_sindescuento=0, descuento=0, precio=0, is_oferta=True)
            detallecompra.save()
            detallecompra_oferta.save()
    oferta_compra.save()

