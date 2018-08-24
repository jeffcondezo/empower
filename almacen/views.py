from django.views.generic import ListView, DetailView
from django.db.models import Sum
from django.shortcuts import redirect, HttpResponse


# Model import-->
from maestro.models import Almacen, Sucursal, Categoria, Proveedor
from .models import Stock, Kardex
from compras.models import OrdenCompra, DetalleOrdenCompra, ResultadoOfertaOrden
# Model import<--

# Form import-->
from compras.forms import CompraForm, DetalleCompraForm, DetalleCompraOfertaForm
# Form import<--

# Utils import-->
from compras.utils import fill_data_compra, recalcular_total_compra, fill_data_compraoferta
# Utils import<--

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
            if self.request.GET['tipo'] != '':
                tipo = self.request.GET['tipo']
                if tipo != '':
                    query = query.filter(tipo_movimiento=tipo)
        if 'fecha_inicio' in self.request.GET and 'fecha_fin' in self.request.GET:
            if self.request.GET['fecha_inicio'] != '' and self.request.GET['fecha_fin'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fecha_inicio'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fecha_fin'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora__gte=fecha_inicio, fechahora__lte=fecha_fin)
        return query


class OrdenListView(BasicEMixin, ListView):

    template_name = 'almacen/ordencompra.html'
    model = OrdenCompra
    nav_name = 'nav_orden'

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
    nav_name = 'nav_kardex'
    view_name = 'orden_compra'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
        context['oferta'] = ResultadoOfertaOrden.objects.filter(detalleorden__ordencompra=self.kwargs['pk'], tipo='1')
        context['orden_id'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.proveedor = orden.proveedor
            compra.almacen = orden.almacen
            compra.asignado = self.request.user
            compra.orden = orden
            compra.save()
            print(compra)
            for i in range(1, int(request.POST['detalle_size'])+1):
                dc_form = DetalleCompraForm(request.POST, prefix='dc'+str(i))
                if dc_form.is_valid():
                    dc_form = dc_form.save(commit=False)
                    dc_form.compra = compra
                    fill_data_compra(dc_form, request.POST['dc'+str(i)+'-id_detalleorden'])
            for i in range(1, int(request.POST['oferta_size'])+1):
                dc_form = DetalleCompraOfertaForm(request.POST, prefix='ro'+str(i))
                if dc_form.is_valid():
                    dc_form = dc_form.save(commit=False)
                    dc_form.compra = compra
                    fill_data_compraoferta(dc_form, request.POST['ro'+str(i)+'-id_resultadooferta'])
            recalcular_total_compra(compra)
            return redirect('/compras/compra/' + str(compra.id))
        else:
            return HttpResponse(form.errors)
