from django.views.generic import ListView
from django.db.models import Sum

# Model import-->
from maestro.models import Almacen, Sucursal, Categoria
from .models import Stock, Kardex
# Model import<--


# Extra python features-->
# Extra python features<--

# Extra python features-->
from maestro.mixin import NavMixin
# Extra python features<--


# Create your views here.
class StockView(NavMixin, ListView):

    template_name = 'almacen/stock.html'
    model = Stock
    nav_name = 'nav_stock'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['almacenes'] = Almacen.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursales')
        almacen = self.request.GET.getlist('almacenes')
        categoria = self.request.GET.getlist('categorias')
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


class KardexView(NavMixin, ListView):

    template_name = 'almacen/kardex.html'
    model = Kardex
    nav_name = 'nav_kardex'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['almacenes'] = Almacen.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        sucursal = self.request.GET.getlist('sucursales')
        almacen = self.request.GET.getlist('almacenes')
        categoria = self.request.GET.getlist('categorias')
        if len(sucursal) > 0:
            query = Kardex.objects.filter(almacen__sucursal__in=Sucursal.objects.filter(pk__in=sucursal))
        elif len(almacen) > 0:
            query = Kardex.objects.filter(almacen__in=Almacen.objects.filter(pk__in=almacen))
        else:
            query = Kardex.objects.all()
        if len(categoria) > 0:
            query = query.filter(producto__categorias__in=categoria)
        if 'tipo' in self.request.GET:
            tipo = self.request.GET['tipo']
            if tipo != '':
                query = query.filter(tipo_movimiento=tipo)
        return query
