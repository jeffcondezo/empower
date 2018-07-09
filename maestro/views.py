from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import redirect, HttpResponse
from django.db.models import Sum

# Model import-->
from maestro.models import Empresa, Sucursal, Almacen, Categoria,\
    Presentacion, Producto, PresentacionxProducto
# Model import<--

# Forms import-->
from .forms import SucursalForm, AlmacenForm, CategoriaForm, PresentacionForm,\
    ProductoForm
# Forms import<--

# Utils import-->
from .utils import format_categories
# Utils import<--

# Extra python features-->
# Extra python features<--

# Extra python features-->
from .mixin import NavMixin
# Extra python features<--


# Views
class SucursalListView(NavMixin, ListView):

    template_name = 'maestro/sucursal-list.html'
    model = Sucursal
    nav_name = 'nav_sucursal'


class SucursalDetailView(NavMixin, DetailView):

    template_name = 'maestro/sucursal-detail.html'
    model = Sucursal
    nav_name = 'nav_sucursal'


class SucursalEditView(NavMixin, TemplateView):

    template_name = 'maestro/sucursal-edit.html'
    nav_name = 'nav_sucursal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = SucursalForm()
        else:
            sucursal = Sucursal.objects.get(pk=self.kwargs['pk'])
            context['object'] = SucursalForm(instance=sucursal)
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


class AlmacenListView(NavMixin, ListView):

    template_name = 'maestro/almacen-list.html'
    model = Almacen
    nav_name = 'nav_almacen'


class AlmacenDetailView(NavMixin, DetailView):

    template_name = 'maestro/almacen-detail.html'
    model = Almacen
    nav_name = 'nav_almacen'


class AlmacenEditView(NavMixin, TemplateView):

    template_name = 'maestro/almacen-edit.html'
    nav_name = 'nav_almacen'

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


class CategoriaListView(NavMixin, ListView):

    template_name = 'maestro/categoria-list.html'
    model = Categoria
    nav_name = 'nav_categoria'
    nav_main = 'nav_main_producto'


class CategoriaDetailView(NavMixin, DetailView):

    template_name = 'maestro/categoria-detail.html'
    model = Categoria
    nav_name = 'nav_categoria'
    nav_main = 'nav_main_producto'


class CategoriaEditView(NavMixin, TemplateView):

    template_name = 'maestro/categoria-edit.html'
    nav_name = 'nav_categoria'
    nav_main = 'nav_main_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = Categoria.objects.none()
        else:
            context['object'] = Categoria.objects.get(pk=self.kwargs['pk'])
        context['categorias'] = Categoria.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = CategoriaForm(request.POST)
        else:
            categoria = Categoria.objects.get(pk=self.kwargs['pk'])
            form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save(commit=False)
            padre = Categoria.objects.get(pk=form.cleaned_data['padre'].pk)
            categoria.nivel = padre.nivel + 1
            categoria.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/categoria')


class PresentacionListView(NavMixin, ListView):

    template_name = 'maestro/presentacion-list.html'
    model = Presentacion
    nav_name = 'nav_presentacion'
    nav_main = 'nav_main_producto'


class PresentacionDetailView(NavMixin, DetailView):

    template_name = 'maestro/categoria-detail.html'
    model = Presentacion
    nav_name = 'nav_presentacion'
    nav_main = 'nav_main_producto'


class PresentacionEditView(NavMixin, TemplateView):

    template_name = 'maestro/presentacion-edit.html'
    nav_name = 'nav_presentacion'
    nav_main = 'nav_main_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = Presentacion.objects.none()
        else:
            context['object'] = Presentacion.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = PresentacionForm(request.POST)
        else:
            presentacion = Presentacion.objects.get(pk=self.kwargs['pk'])
            form = PresentacionForm(request.POST, instance=presentacion)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/presentacion')


class ProductoListView(NavMixin, ListView):

    template_name = 'maestro/producto-list.html'
    model = Producto
    nav_name = 'nav_producto'
    nav_main = 'nav_main_producto'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        categorias = self.request.GET.getlist('categorias')
        if len(categorias) > 0:
            query = Producto.objects.filter(categorias__in=categorias)
        else:
            query = Producto.objects.all()
        return query


class ProductoDetailView(NavMixin, DetailView):

    template_name = 'maestro/producto-detail.html'
    model = Producto
    nav_name = 'nav_producto'
    nav_main = 'nav_main_producto'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = format_categories(Categoria.objects.filter(producto=self.kwargs['pk'])
                                                  .order_by('padre_total', 'nivel'))
        context['presentaciones'] = PresentacionxProducto.objects.filter(producto=self.kwargs['pk'])
        return context


class ProductoEditView(NavMixin, TemplateView):

    template_name = 'maestro/producto-edit.html'
    nav_name = 'nav_producto'
    nav_main = 'nav_main_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = Producto.objects.none()
        else:
            context['object'] = Producto.objects.get(pk=self.kwargs['pk'])
        context['empresas'] = Empresa.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = ProductoForm(request.POST)
        else:
            producto = Producto.objects.get(pk=self.kwargs['pk'])
            form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/producto')


class ProductoCategoriaView(NavMixin, TemplateView):

    template_name = 'maestro/producto-categoria.html'
    nav_name = 'nav_producto'
    nav_main = 'nav_main_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['own_categorias'] = format_categories(Categoria.objects.filter(producto=self.kwargs['pk'])
                                                      .order_by('padre_total', 'nivel'))
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = ProductoForm(request.POST)
        else:
            producto = Producto.objects.get(pk=self.kwargs['pk'])
            form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/maestro/producto')
