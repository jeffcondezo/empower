from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra, Compra, DetalleCompra
from maestro.models import Proveedor, Almacen
# Model import<--

# Forms import-->
from compras.forms import OrdenCompraCreateForm, OrdenCompraEditForm, DetalleOrdenCompraForm, CompraForm,\
    OrdenCompraFiltroForm, OrdenCompraConvertirForm
# Forms import<--

# Utils import-->
from .utils import fill_data, recalcular_total_orden, crear_detallecompra, cargar_resultado_oferta, cargar_oferta,\
    ordentocompra
# Utils import<--

# Extra python features-->
# Extra python features<--

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--


# Views
class OrdenListView(BasicEMixin, ListView):

    template_name = 'compras/orden-list.html'
    model = OrdenCompra
    nav_name = 'nav_orden'
    view_name = 'orden_compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden_filtro'] = OrdenCompraFiltroForm(self.request.GET)
        context['orden_create'] = OrdenCompraCreateForm
        return context

    def get_queryset(self):
        proveedores = self.request.GET.getlist('proveedor')
        estados = self.request.GET.getlist('estado')
        if len(proveedores) > 0:
            query = OrdenCompra.objects.filter(proveedor__in=proveedores)
        else:
            query = OrdenCompra.objects.all()
        if len(estados) > 0:
            query = query.filter(estado__in=estados)
        return query


class OrdenDetailView(BasicEMixin, DetailView):

    template_name = 'compras/orden-detail.html'
    model = OrdenCompra
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        detalle_orden = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
        context['detalle'] = cargar_resultado_oferta(detalle_orden)
        context['orden_convertir'] = OrdenCompraConvertirForm()
        return context


class OrdenCreateView(RedirectView):

    url = '/compras/orden/'
    view_name = 'orden_compra'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        form = OrdenCompraCreateForm(self.request.POST)
        if form.is_valid():
            try:
                orden = OrdenCompra.objects.get(proveedor=form.cleaned_data['proveedor'], estado=1)
            except OrdenCompra.DoesNotExist:
                orden = form.save(commit=False)
                orden.asignado = self.request.user
                orden.save()
            url = self.url + str(orden.id) + '/edit'
        else:
            url = '/compras/orden'
        return url


class OrdenToCompraView(RedirectView):

    url = '/compras/compra/'
    view_name = 'orden_compra'
    action_name = 'tocompra'

    def get_redirect_url(self, *args, **kwargs):
        form = OrdenCompraConvertirForm(self.request.POST)
        if form.is_valid():
            orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
            user = self.request.user
            compra_id = ordentocompra(form, user, orden)
            url = self.url + str(compra_id)
        else:
            return HttpResponse(form.errors)
        return url


class OrdenEditView(BasicEMixin, TemplateView):

    template_name = 'compras/orden-edit.html'
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'actualizar'

    def dispatch(self, request, *args, **kwargs):
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        if orden.estado == '2':
            return redirect('/compras/orden/' + str(orden.id))
        else:
            return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        context['form'] = OrdenCompraEditForm(instance=orden)
        context['model'] = orden
        detalle = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
        content_detalle = []
        for idx, d in enumerate(detalle):
            d = cargar_oferta(d)
            content_detalle.append([DetalleOrdenCompraForm(instance=d, prefix='do'+str(idx+1),
                                                           proveedor=orden.proveedor_id, has_data=True), d])
        context['detalle'] = content_detalle
        context['clean_form'] = DetalleOrdenCompraForm(proveedor=orden.proveedor_id, has_data=False)
        return context

    def post(self, request, *args, **kwargs):
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        form = OrdenCompraEditForm(request.POST, instance=orden)
        if form.is_valid():
            orden = form.save(commit=False)
            if request.POST['detalleorden_to_save'] != '':
                for i in request.POST['detalleorden_to_save'].split(','):
                    if 'do'+i+'-id' in self.request.POST:
                        do = DetalleOrdenCompra.objects.get(pk=self.request.POST['do'+i+'-id'])
                        do_form = DetalleOrdenCompraForm(request.POST, instance=do, prefix='do'+i,
                                                         proveedor=orden.proveedor_id, has_data=True)
                    else:
                        do_form = DetalleOrdenCompraForm(request.POST, prefix='do'+i,
                                                         proveedor=orden.proveedor_id, has_data=True)
                    if do_form.is_valid():
                        do_obj = do_form.save(commit=False)
                        do_obj.ordencompra = orden
                        fill_data(do_obj, request.POST['oferta-'+i])
            if request.POST['detalleorden_to_delete'] != '':
                for j in request.POST['detalleorden_to_delete'].split(','):
                    DetalleOrdenCompra.objects.get(pk=j).delete()
            recalcular_total_orden(orden)
        else:
            return HttpResponse(form.errors)
        return redirect('/compras/orden/'+str(orden.id))


class CompraDetailView(BasicEMixin, DetailView):

    template_name = 'compras/compra-detail.html'
    model = Compra
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = DetalleCompra.objects.filter(compra=self.kwargs['pk'])
        return context
