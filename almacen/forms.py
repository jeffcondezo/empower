from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra, Compra, DetalleCompra
from maestro.models import Producto
# Model import<--


class DetalleCompraForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion', 'total']


class DetalleCompraOfertaForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion']
