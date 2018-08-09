from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra
from maestro.models import Producto
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
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
        }

    def __init__(self, proveedor=False, has_data=False, *args, **kwargs):
        super(DetalleOrdenCompraForm, self).__init__(*args, **kwargs)
        if has_data:
            self.fields['producto'] = forms.ModelChoiceField(
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'default-select2 form-control producto'}),
            )
            self.fields['producto'].empty_label = None
            self.fields['cantidad_presentacion_pedido'] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
        else:
            self.fields['producto'] = forms.ModelChoiceField(
                required=False,
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'form-control producto'}),
            )
            self.fields['cantidad_presentacion_pedido'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
