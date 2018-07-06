from django.views.generic import ListView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum

# Model import-->
from maestro.models import Almacen, Stock
# Model import<--


# Extra python features-->
# Extra python features<--


# Create your views here.

class StockView(ListView, ProcessFormView):

    template_name = 'almacen/stock.html'
    model = Stock

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['almacenes'] = Almacen.objects.all()
        return context

    def get_queryset(self):
        almacen = self.request.GET.getlist('almacenes')
        if len(almacen) > 0:
            query = Stock.objects.filter(almacen__in=Almacen.objects.filter(pk__in=almacen))\
                .values('producto__descripcion').annotate(Sum('cantidad'))
        else:
            query = Stock.objects.all().values('producto__descripcion').annotate(Sum('cantidad'))
            print(query)
        return query
