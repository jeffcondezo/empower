from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, RedirectView

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--

# Model import-->
from clientes.models import Cliente
# Model import<--


# Create your views here.
class ClienteListView(BasicEMixin, ListView):

    template_name = 'clientes/cliente-list.html'
    model = Cliente
    nav_name = 'nav_cliente'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = Cliente.TIPO_CHOICES
        return context

    def get_queryset(self):
        documento = self.request.GET.get('documento', False)
        descripcion = self.request.GET.get('documento', False)
        tipo = self.request.GET.getlist('tipo')
        if documento != '' and documento is not False:
            query = Cliente.objects.filter(documento__icontains=documento)
        elif descripcion != '' and descripcion is not False:
            query = Cliente.objects.filter(descripcion__icontains=descripcion)
        else:
            query = Cliente.objects.all()
        if len(tipo) > 0:
            query = query.filter(tipo__in=tipo)
        return query


class ClienteEditView(BasicEMixin, TemplateView):

    template_name = 'clientes/cliente-edit.html'
    nav_name = 'nav_cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = SucursalForm()
        else:
            sucursal = Sucursal.objects.get(pk=self.kwargs['pk'])
            context['object'] = SucursalForm(instance=sucursal)
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