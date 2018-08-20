from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra, Compra, DetalleCompra
from maestro.models import Proveedor
# Model import<--

# Forms import-->
from compras.forms import OrdenCompraCreateForm, OrdenCompraEditForm, DetalleOrdenCompraForm, CompraForm
# Forms import<--

# Utils import-->
from .utils import fill_data, recalcular_total_orden, crear_detallecompra, cargar_resultado_oferta, cargar_oferta
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
        context['proveedores'] = Proveedor.objects.all()
        context['estados'] = OrdenCompra.ESTADO_CHOICES
        return context

    def get_queryset(self):
        proveedores = self.request.GET.getlist('proveedores')
        estados = self.request.GET.getlist('estados')
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
        return context


class OrdenCreateView(RedirectView):

    url = '/compras/orden/'
    view_name = 'orden_compra'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        form = OrdenCompraCreateForm(self.request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.asignado = self.request.user
            orden.save()
            url = self.url + str(orden.id) + '/edit'
        else:
            url = '/compras/orden'
        return url


class OrdenEditView(BasicEMixin, TemplateView):

    template_name = 'compras/orden-edit.html'
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'actualizar'

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
            return HttpResponse(form.errors[0])
        return redirect('/compras/orden/'+str(orden.id))


class OrdenToCompraView(BasicEMixin, TemplateView):

    template_name = 'compras/orden-tocompra.html'
    nav_name = 'nav_compra'
    view_name = 'orden_compra'
    action_name = 'tocompra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        context['orden'] = orden
        detalle = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
        context['detalle'] = detalle
        context['clean_form'] = DetalleOrdenCompraForm(proveedor=orden.proveedor_id, has_data=False)
        return context

    def post(self, request, *args, **kwargs):
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.asignado = self.request.user
            compra.save()
            detalle_orden = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
            crear_detallecompra(detalle_orden, request.POST, compra)
            orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
            orden.estado = '2'
            orden.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/compras/compra/'+str(compra.id))


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
