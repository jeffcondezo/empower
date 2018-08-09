from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra
from maestro.models import Proveedor
# Model import<--

# Forms import-->
from compras.forms import OrdenCompraCreateForm, OrdenCompraEditForm, DetalleOrdenCompraForm
# Forms import<--

# Utils import-->
from .utils import save_detalleorden
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
        context['detalle'] = DetalleOrdenCompra.objects.filter(ordencompra=self.kwargs['pk'])
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
            content_detalle.append([DetalleOrdenCompraForm(instance=d, proveedor=orden.proveedor_id,
                                                           has_data=True, prefix='do'+str(idx+1)), d])
        context['detalle'] = content_detalle
        context['clean_form'] = DetalleOrdenCompraForm(proveedor=orden.proveedor_id, has_data=False)
        return context

    def post(self, request, *args, **kwargs):
        orden = OrdenCompra.objects.get(pk=self.kwargs['pk'])
        form = OrdenCompraEditForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            for i in request.POST['detalleorden_to_save']:
                if 'do'+i+'-id' in self.request.POST:
                    do = DetalleOrdenCompra.objects.get(pk=self.request.POST['do'+i+'-id'])
                    do_form = DetalleOrdenCompraForm(instance=do, prefix='do'+i)
                else:
                    do_form = DetalleOrdenCompraForm(prefix='do'+i)
                do_obj = do_form.save(commit=False)
                save_detalleorden(do_obj)
        else:
            return HttpResponse(form.errors)
        return redirect('/compras/orden')
