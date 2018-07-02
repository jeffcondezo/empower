from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import redirect, HttpResponse

# Model import-->
from maestro.models import Empresa, Sucursal, Almacen
# Model import<--

# Forms import-->
from .forms import SucursalForm, AlmacenForm
# Forms import<--

# Extra python features-->
# Extra python features<--


# Create your views here.

class SucursalListView(ListView):

    template_name = 'maestro/sucursal-list.html'
    model = Sucursal


class SucursalDetailView(DetailView):

    template_name = 'maestro/sucursal-detail.html'
    model = Sucursal


class SucursalEditView(TemplateView):

    template_name = 'maestro/sucursal-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = Sucursal.objects.none()
        else:
            context['object'] = Sucursal.objects.get(pk=self.kwargs['pk'])
        context['empresas'] = Empresa.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = SucursalForm(request.POST)
        else:
            sucursal = Sucursal.objects.get(pk=self.kwargs['pk'])
            form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/sucursal')


class AlmacenListView(ListView):

    template_name = 'maestro/almacen-list.html'
    model = Almacen


class AlmacenDetailView(DetailView):

    template_name = 'maestro/almacen-detail.html'
    model = Almacen


class AlmacenEditView(TemplateView):

    template_name = 'maestro/almacen-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = Almacen.objects.none()
        else:
            context['object'] = Almacen.objects.get(pk=self.kwargs['pk'])
        context['sucursales'] = Sucursal.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = AlmacenForm(request.POST)
        else:
            almacen = Almacen.objects.get(pk=self.kwargs['pk'])
            form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/almacen')
