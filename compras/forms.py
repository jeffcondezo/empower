from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra
# Model import<--


class OrdenCompraCreateForm(forms.ModelForm):

    class Meta:
        model = OrdenCompra
        fields = ['proveedor']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(OrdenCompraCreateForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = None


class OrdenCompraEditForm(forms.ModelForm):

    class Meta:
        model = OrdenCompra
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(OrdenCompraEditForm, self).__init__(*args, **kwargs)
        self.fields['estado'].empty_label = None


class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion_pedido']
        widgets = {
            'producto': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'presentacionxproducto': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'cantidad_presentacion_pedido': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(DetalleOrdenCompraForm, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = None
        self.fields['presentacionxproducto'].empty_label = None

