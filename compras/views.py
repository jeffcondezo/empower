from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum
from datetime import datetime


# Model import-->
from compras.models import Compra, DetalleCompra
from maestro.models import Proveedor, Almacen
# Model import<--

# Forms import-->
from compras.forms import CompraCreateForm, CompraEditForm, DetalleCompraForm, CompraFiltroForm, ImpuestoForm
# Forms import<--

# Utils import-->
from .utils import fill_data_compra, recalcular_total_compra,\
    cargar_oferta, create_ofertas
# Utils import<--

# Extra python features-->
# Extra python features<--

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--


# Views
class CompraListView(BasicEMixin, ListView):

    template_name = 'compras/compra-list.html'
    model = Compra
    nav_name = 'nav_compra'
    view_name = 'compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compra_filtro'] = CompraFiltroForm(self.request.GET)
        context['compra_create'] = CompraCreateForm()
        return context

    def get_queryset(self):
        query = super().get_queryset()
        proveedores = self.request.GET.getlist('proveedor')
        estados = self.request.GET.getlist('estado')
        tipo = self.request.GET.getlist('tipo')
        if len(proveedores) > 0:
            query = query.filter(proveedor__in=proveedores)
        if len(estados) > 0:
            query = query.filter(estado__in=estados)
        if len(tipo) > 0:
            query = query.filter(tipo__in=tipo)
        if 'fechahora_creacion1' in self.request.GET and 'fechahora_creacion2' in self.request.GET:
            if self.request.GET['fechahora_creacion1'] != '' and self.request.GET['fechahora_creacion2'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fechahora_creacion1'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fechahora_creacion2'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora_creacion__gte=fecha_inicio, fechahora_creacion__lte=fecha_fin)
        if 'total_final1' in self.request.GET or 'total_final2' in self.request.GET:
            monto1 = self.request.GET['total_final1']
            monto2 = self.request.GET['total_final2']
            if monto1 == '':
                query = query.filter(total_final__lte=monto2)
            elif monto2 == '':
                query = query.filter(total_final__gte=monto1)
            else:
                query = query.filter(total_final__gte=monto1, total_final__lte=monto2)
        return query


# class OrdenDetailView(BasicEMixin, DetailView):
#
#     template_name = 'compras/orden-detail.html'
#     model = OrdenCompra
#     nav_name = 'nav_compra'
#     view_name = 'orden_compra'
#     action_name = 'leer'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         detalle_orden = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
#         context['detalle'] = cargar_resultado_oferta(detalle_orden)
#         return context


class CompraCreateView(RedirectView):

    url = '/compras/compra/'
    view_name = 'compra'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        form = CompraCreateForm(self.request.POST)
        if form.is_valid():
            try:
                compra = Compra.objects.get(proveedor=form.cleaned_data['proveedor'], estado=1)
            except Compra.DoesNotExist:
                compra = form.save(commit=False)
                compra.asignado = self.request.user
                compra.save()
            url = self.url + str(compra.id) + '/edit'
        else:
            url = '/compras/compra'
        return url


class CompraEditView(BasicEMixin, TemplateView):

    template_name = 'compras/compra-edit.html'
    nav_name = 'nav_compra'
    view_name = 'compra'
    action_name = 'actualizar'

    def dispatch(self, request, *args, **kwargs):
        compra = Compra.objects.get(pk=self.kwargs['pk'])
        if compra.estado != '1':
            return redirect('/compras/compra/' + str(compra.id))
        else:
            return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = Compra.objects.get(pk=self.kwargs['pk'])
        context['form'] = CompraEditForm(instance=compra)
        context['model'] = compra
        context['impuesto_form'] = ImpuestoForm()
        detalle = DetalleCompra.objects.filter(compra=self.kwargs['pk'], is_oferta=0)
        content_detalle = []
        for idx, d in enumerate(detalle):
            d = cargar_oferta(d)
            content_detalle.append([DetalleCompraForm(instance=d, prefix='dc'+str(idx+1),
                                                      proveedor=compra.proveedor_id, has_data=True), d])
        context['detalle'] = content_detalle
        context['clean_form'] = DetalleCompraForm(proveedor=compra.proveedor_id, has_data=False)
        return context

    def post(self, request, *args, **kwargs):
        compra = Compra.objects.get(pk=self.kwargs['pk'])
        form = CompraEditForm(request.POST, instance=compra)
        if form.is_valid():
            compra = form.save()
            if request.POST['detallecompra_to_save'] != '':
                for i in request.POST['detallecompra_to_save'].split(','):
                    if 'dc'+i+'-id' in self.request.POST:
                        dc = DetalleCompra.objects.get(pk=self.request.POST['dc'+i+'-id'])
                        dc_form = DetalleCompraForm(request.POST, instance=dc, prefix='dc'+i,
                                                    proveedor=compra.proveedor_id, has_data=True)
                    else:
                        dc_form = DetalleCompraForm(request.POST, prefix='dc'+i,
                                                    proveedor=compra.proveedor_id, has_data=True)
                    if dc_form.is_valid():
                        dc_form = dc_form.save(commit=False)
                        dc_form.compra = compra
                        dc_form.save()
                        create_ofertas(request.POST['dc'+i+'-oferta'], dc_form)
                        fill_data_compra(compra, dc_form, request.POST['dc'+i+'-impuesto'])
                    else:
                        return HttpResponse(dc_form.errors)
            if request.POST['detallecompra_to_delete'] != '':
                for j in request.POST['detallecompra_to_delete'].split(','):
                    DetalleCompra.objects.get(pk=j).delete()
        else:
            return HttpResponse(form.errors)
        return redirect('/compras/compra/'+str(compra.id))
