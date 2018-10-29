from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse

# Mixin Import-->
from maestro.mixin import BasicEMixin
# Mixin Import<--

# Extra python features-->
from datetime import datetime
# Extra python features<--
import datetime as dt

# Model import-->
from finanzas.models import Jornada, DetalleJornada, CuentaCliente, CuentaProveedor, PagoCliente, PagoProveedor
from ventas.models import Venta
# Model import<--

# Forms import-->
from finanzas.forms import JornadaFiltroForm, DetalleJornadaCreateForm,\
    JornadaCreateForm, CuentaClienteFiltroForm, PagoClienteCreateForm, CuentaProveedorFiltroForm,\
    PagoProveedorCreateForm, PagoVentaForm
# Forms import<--


class JornadaListView(BasicEMixin, ListView):

    template_name = 'finanzas/jornada-list.html'
    model = Jornada
    nav_name = 'nav_jornada'
    view_name = 'jornada'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jornada_filtro'] = JornadaFiltroForm(self.request.GET)
        context['jornada_open'] = JornadaCreateForm()
        return context

    def get_queryset(self):
        query = super().get_queryset()
        caja = self.request.GET.getlist('caja')
        if len(caja) > 0:
            query = query.filter(caja__in=caja)
        if 'fechahora_inicio1' in self.request.GET and 'fechahora_inicio2' in self.request.GET:
            if self.request.GET['fechahora_inicio1'] != '' and self.request.GET['fechahora_inicio2'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fechahora_inicio1'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fechahora_inicio2'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora_inicio__gte=fecha_inicio, fechahora_inicio__lte=fecha_fin)
        if 'monto1' in self.request.GET or 'monto2' in self.request.GET:
            monto1 = self.request.GET['monto1']
            monto2 = self.request.GET['monto2']
            if monto1 == '':
                query = query.filter(monto_actual__lte=monto2)
            elif monto2 == '':
                query = query.filter(monto_actual__gte=monto1)
            else:
                query = query.filter(monto_actual__gte=monto1, monto_actual__lte=monto2)
        return query


class JornadaDetailView(BasicEMixin, DetailView):

    template_name = 'finanzas/jornada-detail.html'
    model = Jornada
    nav_name = 'nav_jornada'
    view_name = 'jornada'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = DetalleJornada.objects.filter(jornada=self.kwargs['pk'])
        context['djornada_create'] = DetalleJornadaCreateForm()
        return context


class DetalleJornadaCreateView(RedirectView):

    url = '/finanzas/jornada/'
    view_name = 'jornada'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        jornada = Jornada.objects.get(pk=self.kwargs['jornada'])
        form = DetalleJornadaCreateForm(self.request.POST)
        if form.is_valid():
            djornada = form.save(commit=False)
            djornada.asignado = self.request.user
            djornada.jornada = jornada
            djornada.save()
            if djornada.tipo == '1':
                jornada.monto_actual += djornada.monto
            else:
                jornada.monto_actual -= djornada.monto
            jornada.save()
        url = self.url + str(self.kwargs['jornada'])
        return url


class JornadaCloseView(RedirectView):

    url = '/finanzas/jornada/'
    view_name = 'jornada'
    action_name = 'close'

    def get_redirect_url(self, *args, **kwargs):
        jornada = Jornada.objects.get(pk=self.kwargs['jornada'])
        jornada.estado = False
        jornada.save()
        url = self.url + str(self.kwargs['jornada'])
        return url


class JornadaCreateView(RedirectView):

    url = '/finanzas/jornada/'
    view_name = 'jornada'
    action_name = 'close'

    def get_redirect_url(self, *args, **kwargs):
        form = JornadaCreateForm(self.request.POST)
        if form.is_valid():
            try:
                jornada = Jornada.objects.get(caja=form.cleaned_data['caja'], estado=True)
            except Jornada.DoesNotExist:
                jornada = form.save(commit=False)
                jornada.asignado_inicio = self.request.user
                jornada.monto_actual = jornada.monto_apertura
                jornada.save()
        url = self.url + str(jornada.id)
        return url


class CuentaClienteListView(BasicEMixin, ListView):

    template_name = 'finanzas/cuentacliente-list.html'
    model = CuentaCliente
    nav_name = 'nav_cuentacliente'
    view_name = 'cuentacliente'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuentacliente_filtro'] = CuentaClienteFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        cliente = self.request.GET.getlist('cliente')
        duracion = self.request.GET.getlist('duracion')
        estado = self.request.GET.getlist('estado')
        tipo = self.request.GET.getlist('tipo')
        if len(cliente) > 0:
            query = query.filter(cliente__in=cliente)
        if len(duracion) > 0:
            query = query.filter(duracion__in=duracion)
        if len(estado) > 0:
            query = query.filter(estado__in=estado)
        if len(tipo) > 0:
            query = query.filter(tipo__in=tipo)
        if 'fechahora_caducidad1' in self.request.GET and 'fechahora_caducidad2' in self.request.GET:
            if self.request.GET['fechahora_caducidad1'] != '' and self.request.GET['fechahora_caducidad2'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fechahora_caducidad1'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fechahora_caducidad2'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora_caducidad__gte=fecha_inicio, fechahora_caducidad__lte=fecha_fin)
        if 'monto_amortizado1' in self.request.GET or 'monto_amortizado2' in self.request.GET:
            monto_amortizado1 = self.request.GET['monto_amortizado1']
            monto_amortizado2 = self.request.GET['monto_amortizado2']
            if monto_amortizado1 == '':
                query = query.filter(monto_amortizado__lte=monto_amortizado2)
            elif monto_amortizado2 == '':
                query = query.filter(monto_amortizado__gte=monto_amortizado1)
            else:
                query = query.filter(monto_amortizado__gte=monto_amortizado1, monto_amortizado__lte=monto_amortizado2)
        if 'monto_total1' in self.request.GET or 'monto_total2' in self.request.GET:
            monto_total1 = self.request.GET['monto_total1']
            monto_total2 = self.request.GET['monto_total2']
            if monto_total1 == '':
                query = query.filter(monto_total__lte=monto_total2)
            elif monto_total2 == '':
                query = query.filter(monto_total__gte=monto_total1)
            else:
                query = query.filter(monto_total__gte=monto_total1, monto_total__lte=monto_total2)
        return query


class CuentaClienteDetailView(BasicEMixin, DetailView):

    template_name = 'finanzas/cuentacliente-detail.html'
    model = CuentaCliente
    nav_name = 'nav_cuentacliente'
    view_name = 'cuentacliente'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = PagoCliente.objects.filter(cuentacliente=self.kwargs['pk'])
        context['pago_create'] = PagoClienteCreateForm()
        return context


class PagoClienteCreateView(RedirectView):

    url = '/finanzas/cuentacliente/'
    view_name = 'pago'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        cuentacliente = CuentaCliente.objects.get(pk=self.kwargs['cuentacliente'])
        form = PagoClienteCreateForm(self.request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.asignado = self.request.user
            pago.cuentacliente = cuentacliente
            pago.save()
            cuentacliente.monto_amortizado += pago.monto
            cuentacliente.save()
        url = self.url + str(self.kwargs['cuentacliente'])
        return url


class CuentaProveedorListView(BasicEMixin, ListView):

    template_name = 'finanzas/cuentaproveedor-list.html'
    model = CuentaProveedor
    nav_name = 'nav_cuentaproveedor'
    view_name = 'cuentaproveedor'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuentaproveedor_filtro'] = CuentaProveedorFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        cliente = self.request.GET.getlist('cliente')
        duracion = self.request.GET.getlist('duracion')
        estado = self.request.GET.getlist('estado')
        tipo = self.request.GET.getlist('tipo')
        if len(cliente) > 0:
            query = query.filter(cliente__in=cliente)
        if len(duracion) > 0:
            query = query.filter(duracion__in=duracion)
        if len(estado) > 0:
            query = query.filter(estado__in=estado)
        if len(tipo) > 0:
            query = query.filter(tipo__in=tipo)
        if 'fechahora_caducidad1' in self.request.GET and 'fechahora_caducidad2' in self.request.GET:
            if self.request.GET['fechahora_caducidad1'] != '' and self.request.GET['fechahora_caducidad2'] != '':
                fecha_inicio = datetime.strptime(self.request.GET['fechahora_caducidad1'], '%d/%m/%Y %H:%M')
                fecha_fin = datetime.strptime(self.request.GET['fechahora_caducidad2'], '%d/%m/%Y %H:%M')
                query = query.filter(fechahora_caducidad__gte=fecha_inicio, fechahora_caducidad__lte=fecha_fin)
        if 'monto_amortizado1' in self.request.GET or 'monto_amortizado2' in self.request.GET:
            monto_amortizado1 = self.request.GET['monto_amortizado1']
            monto_amortizado2 = self.request.GET['monto_amortizado2']
            if monto_amortizado1 == '':
                query = query.filter(monto_amortizado__lte=monto_amortizado2)
            elif monto_amortizado2 == '':
                query = query.filter(monto_amortizado__gte=monto_amortizado1)
            else:
                query = query.filter(monto_amortizado__gte=monto_amortizado1, monto_amortizado__lte=monto_amortizado2)
        if 'monto_total1' in self.request.GET or 'monto_total2' in self.request.GET:
            monto_total1 = self.request.GET['monto_total1']
            monto_total2 = self.request.GET['monto_total2']
            if monto_total1 == '':
                query = query.filter(monto_total__lte=monto_total2)
            elif monto_total2 == '':
                query = query.filter(monto_total__gte=monto_total1)
            else:
                query = query.filter(monto_total__gte=monto_total1, monto_total__lte=monto_total2)
        return query


class CuentaProveedorDetailView(BasicEMixin, DetailView):

    template_name = 'finanzas/cuentaproveedor-detail.html'
    model = CuentaProveedor
    nav_name = 'nav_cuentaproveedor'
    view_name = 'cuentaproveedor'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle'] = PagoProveedor.objects.filter(cuentaproveedor=self.kwargs['pk'])
        context['pago_create'] = PagoProveedorCreateForm()
        return context


class PagoProveedorCreateView(RedirectView):

    url = '/finanzas/cuentaproveedor/'
    view_name = 'pago'
    action_name = 'crear'

    def get_redirect_url(self, *args, **kwargs):
        cuentaproveedor = CuentaProveedor.objects.get(pk=self.kwargs['cuentaproveedor'])
        form = PagoProveedorCreateForm(self.request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.asignado = self.request.user
            pago.cuentaproveedor = cuentaproveedor
            pago.save()
            cuentaproveedor.monto_amortizado += pago.monto
            cuentaproveedor.save()
        url = self.url + str(self.kwargs['cuentaproveedor'])
        return url


class VentaPagoView(RedirectView):

    url = '/ventas/venta/'
    view_name = 'finanzas'
    action_name = 'venta_pago'

    def get_redirect_url(self, *args, **kwargs):
        venta = Venta.objects.get(pk=self.kwargs['venta'])
        form = PagoVentaForm(self.request.POST, instance=venta)
        if not venta.is_pagado:
            if form.is_valid():
                venta = form.save(commit=False)
                venta.is_pagado = True
                fecha_actual = datetime.now()
                if form.cleaned_data['duracion'] == '1':
                    fecha_final = fecha_actual + dt.timedelta(days=7)
                elif form.cleaned_data['duracion'] == '2':
                    fecha_final = fecha_actual + dt.timedelta(days=14)
                elif form.cleaned_data['duracion'] == '3':
                    fecha_final = fecha_actual + dt.timedelta(days=21)
                elif form.cleaned_data['duracion'] == '4':
                    fecha_final = fecha_actual + dt.timedelta(days=30)
                tipo = form.cleaned_data['tipo_pago']
                pago = form.cleaned_data['pago']
                if venta.cliente is not None:
                    if tipo == '2':
                        if venta.total_final == pago:
                            venta.tipo_pago = '1'
                            venta.estado_pago = '2'
                            estado = '2'
                        elif venta.total_final > pago:
                            venta.estado_pago = '1'
                            estado = '1'
                    else:
                        venta.estado_pago = '2'
                        estado = '2'
                    cuentacliente = CuentaCliente(duracion=form.cleaned_data['duracion'], tipo=tipo,
                                                  estado=estado, fechahora_caducidad=fecha_final,
                                                  monto_total=venta.total_final, monto_amortizado=pago,
                                                  cliente=venta.cliente)
                    cuentacliente.save()
                    PagoCliente(tipo='1', monto=pago, cuentacliente=cuentacliente, asignado=self.request.user).save()
                else:
                    venta.tipo_pago = '1'
                    venta.estado_pago = '2'
                jornada = Jornada.objects.get(pk=4)
                DetalleJornada(jornada=jornada, tipo='1', target=venta.id, monto=pago, descripcion='Venta',
                               asignado=self.request.user).save()
                venta.save()
            url = self.url + str(venta.id) + '/edit'
        else:
            url = '/ventas/venta'
        return url
