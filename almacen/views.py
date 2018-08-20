from django.views.generic import ListView, DetailView
from django.db.models import Sum

# Model import-->
from maestro.models import Almacen, Sucursal, Categoria, Proveedor
from .models import Stock, Kardex
from compras.models import OrdenCompra, DetalleOrdenCompra, ResultadoOfertaOrden
# Model import<--


# Extra python features-->
from datetime import datetime
# Extra python features<--

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--


# Create your views here.
class StockView(BasicEMixin, ListView):

    template_name = 'almacen/stock.html'
    model = Stock
    nav_name = 'nav_stock'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['almacenes'] = Almacen.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursales')
        almacen = self.request.GET.getlist('almacenes')
        categoria = self.request.GET.getlist('categorias')
        if len(sucursal) > 0:
            query = Stock.objects.filter(almacen__sucursal__in=Sucursal.objects.filter(pk__in=sucursal))
        elif len(almacen) > 0:
            query = Stock.objects.filter(almacen__in=Almacen.objects.filter(pk__in=almacen))
        else:
            query = Stock.objects.all()
        if len(categoria) > 0:
            query = query.filter(producto__categorias__in=categoria)
        query = query.values('producto__descripcion').annotate(Sum('cantidad'))
        return query


class KardexView(BasicEMixin, ListView):

    template_name = 'almacen/kardex.html'
    model = Kardex
    nav_name = 'nav_kardex'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['almacenes'] = Almacen.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursales')
        almacen = self.request.GET.getlist('almacenes')
        categoria = self.request.GET.getlist('categorias')
        if len(sucursal) > 0:
            query = Kardex.objects.filter(almacen__sucursal__in=Sucursal.objects.filter(pk__in=sucursal))
        elif len(almacen) > 0:
            query = Kardex.objects.filter(almacen__in=Almacen.objects.filter(pk__in=almacen))
        else:
            query = Kardex.objects.all()
        if len(categoria) > 0:
            query = query.filter(producto__categorias__in=categoria)
        if 'tipo' in self.request.GET:
            tipo = self.request.GET['tipo']
            if tipo != '':
                query = query.filter(tipo_movimiento=tipo)
        if 'fecha_inicio' in self.request.GET and 'fecha_fin' in self.request.GET:
            fecha_inicio = datetime.strptime(self.request.GET['fecha_inicio'], '%d/%m/%Y %H:%M')
            fecha_fin = datetime.strptime(self.request.GET['fecha_fin'], '%d/%m/%Y %H:%M')
            query = query.filter(fechahora__gte=fecha_inicio, fechahora__lte=fecha_fin)
        return query


class OrdenListView(BasicEMixin, ListView):

    template_name = 'almacen/ordencompra.html'
    model = OrdenCompra
    nav_name = 'nav_orden'
    view_name = 'orden_compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedores'] = Proveedor.objects.all()
        context['estados'] = OrdenCompra.ESTADO_CHOICES
        return context

    def get_queryset(self):
        proveedores = self.request.GET.getlist('proveedores')
        query = OrdenCompra.objects.filter(estado='2')
        if len(proveedores) > 0:
            query = query.filter(proveedor__in=proveedores)
        return query


class OrdenDetailView(BasicEMixin, DetailView):

    template_name = 'almacen/recepcion.html'
    model = OrdenCompra
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
        context['oferta'] = ResultadoOfertaOrden.objects.filter(detalleorden__ordencompra=self.kwargs['pk'], tipo='1')
        return context