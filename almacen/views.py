from django.views.generic import ListView, DetailView
from django.db.models import Sum
from django.shortcuts import redirect, HttpResponse


# Model import-->
from maestro.models import Almacen, Sucursal, Categoria, Proveedor
from .models import Stock, Kardex
from compras.models import Compra, DetalleCompra
from ventas.models import Venta, DetalleVenta
# Model import<--

# Form import-->
from compras.forms import DetalleCompraRecepcionForm, DetalleCompraNoDeseadoForm, CompraRecepcionForm
from almacen.forms import StockFiltroForm, KardexFiltroForm, RecepcionFiltroForm
from ventas.forms import VentaEntregaForm, DetalleVentaEntregaForm
# Form import<--

# Utils import-->
from compras.utils import fill_data_detallecompra
from almacen.utils import loadtax
from ventas.utils import fill_data_detalleventa
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
        context['stock_filtro'] = StockFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursal')
        almacen = self.request.GET.getlist('almacen')
        categoria = self.request.GET.getlist('categoria')
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
        context['kardex_filtro'] = KardexFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursales')
        almacen = self.request.GET.getlist('almacenes')
        categoria = self.request.GET.getlist('categorias')
        tipo = self.request.GET.getlist('tipo')
        if len(sucursal) > 0:
            query = Kardex.objects.filter(almacen__sucursal__in=Sucursal.objects.filter(pk__in=sucursal))
        elif len(almacen) > 0:
            query = Kardex.objects.filter(almacen__in=Almacen.objects.filter(pk__in=almacen))
        else:
            query = Kardex.objects.all()
        if len(categoria) > 0:
            query = query.filter(producto__categorias__in=categoria)
        if len(tipo) > 0:
            query = query.filter(tipo_movimiento__in=tipo)
        if 'fecha_inicio' in self.request.GET and 'fecha_fin' in self.request.GET:
            if self.request.GET['fecha_inicio'] != '' and self.request.GET['fecha_fin'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fecha_inicio'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fecha_fin'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora__gte=fecha_inicio, fechahora__lte=fecha_fin)
        query.order_by('fechahora')
        return query


class RecepcionCompraListView(BasicEMixin, ListView):

    template_name = 'almacen/recepcion_compra-list.html'
    model = Compra
    nav_name = 'nav_recepcion_compra'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recepcion_filtro'] = RecepcionFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        proveedores = self.request.GET.getlist('proveedor')
        query = Compra.objects.filter(tipo='2', estado='2')
        if len(proveedores) > 0:
            query = query.filter(proveedor__in=proveedores)
        return query


class RecepcionCompraEditView(BasicEMixin, DetailView):

    template_name = 'almacen/recepcion_compra-edit.html'
    model = Compra
    nav_name = 'nav_recepcion_compra'
    view_name = 'recepcion_compra'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        detalle_compra = DetalleCompra.objects.filter(compra=self.kwargs['pk'])
        for d in detalle_compra:
            d = loadtax(d)
        context['detalle'] = detalle_compra
        context['compra_form'] = CompraRecepcionForm(instance=context['object'])
        context['clean_form'] = DetalleCompraNoDeseadoForm(proveedor=context['object'].proveedor_id)
        return context

    def post(self, request, *args, **kwargs):
        compra = Compra.objects.get(pk=self.kwargs['pk'])
        form = CompraRecepcionForm(request.POST, instance=compra)
        if form.is_valid():
            compra = form.save()
            if request.POST['detallecompra_to_save'] != '':
                for i in request.POST['detallecompra_to_save'].split(','):
                    if 'dc'+i+'-id' in self.request.POST:
                        if self.request.POST['dc'+i+'-id'] != '':
                            dc = DetalleCompra.objects.get(pk=self.request.POST['dc'+i+'-id'])
                            dc_form = DetalleCompraRecepcionForm(request.POST, instance=dc, prefix='dc'+i)
                        else:
                            dc_form = DetalleCompraNoDeseadoForm(request.POST, prefix='dc'+i,
                                                                 proveedor=compra.proveedor_id)
                    if dc_form.is_valid():
                        dc_obj = dc_form.save(commit=False)
                        dc_obj.compra = compra
                        fill_data_detallecompra(dc_obj, compra.estado, compra)
            if request.POST['detallecompra_to_delete'] != '':
                for j in request.POST['detallecompra_to_delete'].split(','):
                    detalle_compra = DetalleCompra.objects.get(pk=j)
                    if detalle_compra.is_nodeseado:
                        detalle_compra.delete()
            return redirect('/compras/compra/' + str(compra.id))
        else:
            return HttpResponse(form.errors)


class EntregaVentaListView(BasicEMixin, ListView):

    template_name = 'almacen/entrega_venta-list.html'
    model = Compra
    nav_name = 'nav_entrega_venta'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entrega_filtro'] = RecepcionFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        clientes = self.request.GET.getlist('cliente')
        query = Venta.objects.filter(tipo='2', estado='2')
        if len(clientes) > 0:
            query = query.filter(cliente__in=clientes)
        return query


class EntregaVentaEditView(BasicEMixin, DetailView):

    template_name = 'almacen/entrega_venta-edit.html'
    model = Venta
    nav_name = 'nav_entrega_venta'
    view_name = 'entrega_venta'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        detalle_venta = DetalleVenta.objects.filter(venta=self.kwargs['pk'])
        for d in detalle_venta:
            d = loadtax(d)
        context['detalle'] = detalle_venta
        context['venta_form'] = VentaEntregaForm(instance=context['object'])
        return context

    def post(self, request, *args, **kwargs):
        venta = Venta.objects.get(pk=self.kwargs['pk'])
        form = VentaEntregaForm(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save()
            if request.POST['detalleventa_to_save'] != '':
                for i in request.POST['detalleventa_to_save'].split(','):
                    if 'dv'+i+'-id' in self.request.POST:
                        if self.request.POST['dv'+i+'-id'] != '':
                            dv = DetalleVenta.objects.get(pk=self.request.POST['dv'+i+'-id'])
                            dv_form = DetalleVentaEntregaForm(request.POST, instance=dv, prefix='dv'+i)
                    if dv_form.is_valid():
                        dv_obj = dv_form.save(commit=False)
                        dv_obj.venta = venta
                        fill_data_detalleventa(dv_obj, venta.estado, venta)
            return redirect('/ventas/venta/' + str(venta.id))
        else:
            return HttpResponse(form.errors)
