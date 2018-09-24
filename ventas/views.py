from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import redirect, HttpResponse

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--

# Model import-->
from ventas.models import OfertaVenta
# Model import<--

# Forms import-->
from .forms import OfertaVentaForm
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
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/producto')
