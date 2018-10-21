from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import Compra, DetalleCompra
from maestro.models import Producto, Categoria, Sucursal, Almacen, Proveedor
from .models import Stock, Kardex
from clientes.models import Cliente
# Model import<--


class DetalleCompraForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_pedido', 'total']


class DetalleCompraOfertaForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_pedido']


class StockFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(StockFiltroForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['categoria'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.all(), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['almacen'] = forms.ModelChoiceField(queryset=Almacen.objects.all(), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['almacen'].empty_label = None


class KardexFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(KardexFiltroForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['categoria'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.all(), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['almacen'] = forms.ModelChoiceField(queryset=Almacen.objects.all(), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['almacen'].empty_label = None
        self.fields['tipo'] = forms.ChoiceField(choices=Kardex.TIPO_MOVIMIENTO_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                    attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fecha_inicio'] = forms.CharField(required=False,
                                                      widget=forms.TextInput(
                                                          attrs={'id': 'fecha_inicio', 'placeholder': 'Inicio',
                                                                 'class': 'form-control'}))
        self.fields['fecha_fin'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(
                                                       attrs={'id': 'fecha_fin', 'placeholder': 'Fin',
                                                              'class': 'form-control'}))


class RecepcionFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RecepcionFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None


class EntregaFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(EntregaFiltroForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['cliente'].empty_label = None
