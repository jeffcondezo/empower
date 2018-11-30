from .models import PagoProveedor, CuentaProveedor
import json
from datetime import datetime


def cerrarnota(nota, asignado):
    if nota.estado != '2':
        nota.estado = '2'
        nota.fechahora_cierre = datetime.now()
        nota.save()
        cuentaproveedor = CuentaProveedor.objects.get(compra=nota.compra)
        PagoProveedor(tipo='4', monto=nota.monto, cuentaproveedor=cuentaproveedor, asignado=asignado).save()
        cuentaproveedor.monto_amortizado += nota.monto
        cuentaproveedor.monto_deuda -= nota.monto
        if cuentaproveedor.monto_deuda == 0:
            cuentaproveedor.estado = '2'
        cuentaproveedor.save()
        url = '/'
    else:
        url = '/?incidencias=' + json.dumps([
            ['3', 'Ya se Cerró']])
    return url

