from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse

# Mixin Import-->
from maestro.mixin import BasicEMixin
# Mixin Import<--

# Extra python features-->
from datetime import datetime
# Extra python features<--

from .utils import fill_data_venta

# Model import-->
from ventas.models import OfertaVenta, Venta, DetalleVenta
# Model import<--

# Forms import-->
from .forms import OfertaVentaForm, VentaFiltroForm, VentaCreateForm, VentaEditForm, DetalleVentaForm, ImpuestoForm
# Forms import<--


# Create your views here.
class OfertaListView(BasicEMixin, ListView):

    template_name = 'ventas/oferta-list.html'
    model = OfertaVenta
    nav_name = 'nav_oferta'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        categorias = self.request.GET.getlist('categoria')
        if len(categorias) > 0:
            query = OfertaVenta.objects.filter(categorias__in=categorias)
        else:
            query = OfertaVenta.objects.all()
        return query


class OfertaDetailView(BasicEMixin, DetailView):

    template_name = 'ventas/oferta-detail.html'
    model = OfertaVenta
    nav_name = 'nav_oferta'


class OfertaEditView(BasicEMixin, TemplateView):

    template_name = 'ventas/oferta-edit.html'
    nav_name = 'nav_oferta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
                context['object'] = OfertaVentaForm
        else:
            producto = OfertaVenta.objects.get(pk=self.kwargs['pk'])
            context['object'] = OfertaVentaForm(instance=producto)
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = OfertaVentaForm(request.POST)
        else:
            producto = OfertaVenta.objects.get(pk=self.kwargs['pk'])
            form = OfertaVentaForm(request.POST, instance=producto)
        if form.is_valid():
            oferta = form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/ventas/oferta/' + str(oferta.id))


class VentaListView(BasicEMixin, ListView):

    template_name = 'ventas/venta-list.html'
    model = Venta
    nav_name = 'nav_venta'
    view_name = 'venta'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venta_filtro'] = VentaFiltroForm(self.request.GET)
        context['venta_create'] = VentaCreateForm()
        return context

    def get_queryset(self):
        Venta.objects.filter()
        query = super().get_queryset()
        cliente = self.request.GET.getlist('cliente')
        sucursal = self.request.GET.getlist('sucursal')
        estado = self.request.GET.getlist('estado')
        tipo_pago = self.request.GET.getlist('tipo_pago')
        estado_pago = self.request.GET.getlist('estado_pago')
        if len(cliente) > 0:
            query = query.filter(cliente__in=cliente)
        if len(sucursal) > 0:
            query = query.filter(sucursal__in=sucursal)
        if len(estado) > 0:
            query = query.filter(estado__in=estado)
        if len(tipo_pago) > 0:
            query = query.filter(tipo_pago__in=tipo_pago)
        if len(estado_pago) > 0:
            query = query.filter(estado_pago__in=estado_pago)
        if 'fechahora_creacion1' in self.request.GET and 'fechahora_creacion2' in self.request.GET:
            if self.request.GET['fechahora_creacion1'] != '' and self.request.GET['fechahora_creacion2'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fechahora_creacion1'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fechahora_creacion2'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora_creacion__gte=fecha_inicio, fechahora_creacion__lte=fecha_fin)
        if 'total1' in self.request.GET or 'total2' in self.request.GET:
            total1 = self.request.GET['total1']
            total2 = self.request.GET['total2']
            if total1 == '':
                query = query.filter(total__lte=total2)
            elif total2 == '':
                query = query.filter(total__gte=total1)
            else:
                query = query.filter(total__gte=total1, total__lte=total2)
        return query


class VentaCreateView(RedirectView):

    url = '/ventas/venta/'
    view_name = 'venta'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        form = VentaCreateForm(self.request.POST)
        if form.is_valid():
            try:
                venta = Venta.objects.get(cliente=form.cleaned_data['cliente'], estado=1)
            except Venta.DoesNotExist:
                venta = form.save(commit=False)
                venta.asignado = self.request.user
                venta.save()
            url = self.url + str(venta.id) + '/edit'
        else:
            url = '/ventas/venta'
        return url


class VentaEditView(BasicEMixin, TemplateView):

    template_name = 'ventas/venta-edit.html'
    nav_name = 'nav_venta'
    view_name = 'orden_compra'
    action_name = 'actualizar'

    def dispatch(self, request, *args, **kwargs):
        venta = Venta.objects.get(pk=self.kwargs['pk'])
        if venta.estado == '2':
            return redirect('/ventas/venta/' + str(venta.id))
        else:
            return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = Venta.objects.get(pk=self.kwargs['pk'])
        context['form'] = VentaEditForm(instance=venta)
        context['impuesto_form'] = ImpuestoForm()
        context['model'] = venta
        context['detalle'] = DetalleVenta.objects.filter(venta=self.kwargs['pk'])
        context['clean_form'] = DetalleVentaForm(sucursal=venta.sucursal_id, has_data=False)
        return context

    def post(self, request, *args, **kwargs):
        venta = Venta.objects.get(pk=self.kwargs['pk'])
        form = VentaEditForm(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save(commit=False)
            if request.POST['detalleventa_to_save'] != '':
                for i in request.POST['detalleventa_to_save'].split(','):
                    if 'dv'+i+'-id' in self.request.POST:
                        dv = DetalleVenta.objects.get(pk=self.request.POST['dv'+i+'-id'])
                        dv_form = DetalleVentaForm(request.POST, instance=dv, prefix='dv'+i,
                                                   sucursal=venta.sucursal_id, has_data=True)
                    else:
                        dv_form = DetalleVentaForm(request.POST, prefix='dv'+i,
                                                   sucursal=venta.sucursal_id, has_data=True)
                    if dv_form.is_valid():
                        dv_form = dv_form.save(commit=False)
                        dv_form.venta = venta
                        fill_data_venta(venta, dv_form, request.POST['dv'+i+'-impuesto_inp'])
                    else:
                        return HttpResponse(dv_form.errors)
            if request.POST['detalleventa_to_delete'] != '':
                for j in request.POST['detalleventa_to_delete'].split(','):
                    DetalleVenta.objects.get(pk=j).delete()
        else:
            return HttpResponse(form.errors)
        return redirect('/compras/orden/'+str(venta.id))