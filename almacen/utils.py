from almacen.models import Kardex, Stock
from maestro.models import Almacen, PresentacionxProducto
import json


def update_kardex_stock(detalle, tipo_movimiento, tipo_detalle, obj):
    if tipo_detalle == '2' or tipo_detalle == '4':
        almacen = Almacen.objects.filter(sucursal=obj.sucursal_id)[0]
    elif tipo_detalle == '1':
        almacen = Almacen.objects.get(pk=obj.almacen_id)
    try:
        stock = Stock.objects.get(producto=detalle.producto_id, almacen=almacen.id)
    except Stock.DoesNotExist:
        stock = Stock(producto=detalle.producto, almacen=almacen, cantidad=0)
    if tipo_movimiento == '1':
        if detalle.cantidad_unidad_entrega > detalle.cantidad_unidad_pedido:
            cantidad_trabajo = detalle.cantidad_unidad_pedido
            cantidad_stock = stock.cantidad + cantidad_trabajo
        else:
            cantidad_trabajo = detalle.cantidad_unidad_entrega
            cantidad_stock = stock.cantidad + cantidad_trabajo
    elif tipo_movimiento == '2':
        cantidad_trabajo = detalle.cantidad_unidad_entrega
        cantidad_stock = stock.cantidad - cantidad_trabajo
        if cantidad_stock < 0:
            cantidad_stock = 0
    stock.cantidad = cantidad_stock
    stock.save()
    kardex = Kardex(almacen=almacen, producto=detalle.producto, tipo_movimiento=tipo_movimiento,
                    tipo_detalle=tipo_detalle, cantidad=cantidad_trabajo)
    if tipo_movimiento == '1':
        if tipo_detalle == '1':
            kardex.detallecompra = detalle
        elif tipo_detalle == '4':
            kardex.detalleventa = detalle
        kardex.cantidad_entrada = kardex.cantidad
        kardex.precio_unitario_entrada = detalle.total_final / cantidad_trabajo
        kardex.total_entrada = detalle.total_final
        kardex.cantidad_saldo = cantidad_stock
        kardex.precio_unitario_saldo = kardex.precio_unitario_entrada
        kardex.total_saldo = cantidad_stock * kardex.precio_unitario_saldo
        kardex.tipo_comprobante = obj.tipo_comprobante
        kardex.serie_comprobante = obj.serie_comprobante
        kardex.numero_comprobante = obj.numero_comprobante
    elif tipo_movimiento == '2':
        if tipo_detalle == '2':
            kardex.detalleventa = detalle
        elif tipo_detalle == '3':
            kardex.detallecompra = detalle
        kardex.cantidad_entrada = kardex.cantidad
        kardex.precio_unitario_salida = detalle.total_final / cantidad_trabajo
        kardex.total_salida = detalle.total_final
        kardex.cantidad_saldo = cantidad_stock
        kardex.precio_unitario_saldo = kardex.precio_unitario_salida
        kardex.total_saldo = cantidad_stock * kardex.precio_unitario_saldo
        kardex.tipo_comprobante = obj.tipo_comprobante
        kardex.serie_comprobante = obj.serie_comprobante
        kardex.numero_comprobante = obj.numero_comprobante
    kardex.save()


def loadtax(d):
    impuestos_model = d.impuesto.all()
    impuestos = []
    total = 0
    for i in impuestos_model:
        impuestos.append(i.descripcion+" - "+str(i.porcentaje)+"%")
        total += i.porcentaje
    d.impuesto_value = [impuestos, total]
    return d


def loadstockdetail(stock):
    for s in stock:
        presentacionesxproducto = PresentacionxProducto.objects.filter(producto=s['producto__id']).order_by('-cantidad')
        cantidad = s['cantidad__sum']
        string = ''
        for p in presentacionesxproducto:
            temp_cant = cantidad // p.cantidad
            if temp_cant > 0:
                string += str(temp_cant) + ' ' + p.presentacion.descripcion + ' // '
                cantidad -= temp_cant * p.cantidad
        s['stock_detail'] = string[:-3]
    return stock


def update_kardex_stock_notacredito(detalle, obj):
    almacen = Almacen.objects.get(pk=obj.compra.almacen_id)
    try:
        stock = Stock.objects.get(producto=detalle.producto_id, almacen=almacen.id)
    except Stock.DoesNotExist:
        stock = Stock(producto=detalle.producto, almacen=almacen, cantidad=0)
    cantidad_stock = stock.cantidad + detalle.cantidad_unidad_nota
    stock.cantidad = cantidad_stock
    stock.save()
    kardex = Kardex(almacen=almacen, producto=detalle.producto, tipo_movimiento=1,
                    tipo_detalle=5, cantidad=detalle.cantidad_unidad_nota)
    kardex.detallenota = detalle
    kardex.cantidad_entrada = kardex.cantidad
    kardex.precio_unitario_entrada = detalle.total / detalle.cantidad_unidad_nota
    kardex.total_entrada = detalle.total
    kardex.cantidad_saldo = cantidad_stock
    kardex.precio_unitario_saldo = kardex.precio_unitario_entrada
    kardex.total_saldo = cantidad_stock * kardex.precio_unitario_saldo
    kardex.tipo_comprobante = obj.tipo_comprobante
    kardex.serie_comprobante = obj.serie_comprobante
    kardex.numero_comprobante = obj.numero_comprobante
    kardex.save()
