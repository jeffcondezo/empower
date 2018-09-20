from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import OrdenCompra, DetalleOrdenCompra, Compra, DetalleCompra
from maestro.models import Producto, Proveedor, TipoComprobante
# Model import<--


class OrdenCompraCreateForm(forms.ModelForm):

    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'almacen']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'almacen': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(OrdenCompraCreateForm, self).__init__(*args, **kwargs)
        self.fields['almacen'].empty_label = None
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
        self.fields['estado'].choices = [i for i in self.fields['estado'].choices if i[0] in ['1', '4']]


class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion', 'precio']
        widgets = {
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
        }

    def __init__(self, *args, **kwargs):
        has_data = kwargs.pop('has_data')
        proveedor = kwargs.pop('proveedor')
        super(DetalleOrdenCompraForm, self).__init__(*args, **kwargs)
        if has_data:
            self.fields['producto'] = forms.ModelChoiceField(
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'default-select2 form-control producto'}),
            )
            self.fields['producto'].empty_label = None
            self.fields['cantidad_presentacion'] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
            self.fields['precio'] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control precio'})
            )
        else:
            self.fields['producto'] = forms.ModelChoiceField(
                required=False,
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'form-control producto'}),
            )
            self.fields['cantidad_presentacion'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
            self.fields['precio'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control precio'})
            )


class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['estado', 'tipo_comprobante', 'serie_comprobante', 'numero_comprobante', 'tipo_pago']
        widgets = {
            'estado': forms.Select(attrs={'class': 'select2 form-control'}),
            'tipo_comprobante': forms.Select(attrs={'class': 'select2 form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2 form-control'}),
            'serie_comprobante': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_comprobante': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Sirve para el modal de agregar un no deseado a la compra.
class DetalleCompraNoDeseadoForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion_entrega', 'total_final']
        widgets = {
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
        }

    def __init__(self, *args, **kwargs):
        proveedor = kwargs.pop('proveedor')
        super(DetalleCompraNoDeseadoForm, self).__init__(*args, **kwargs)
        self.fields['producto'] = forms.ModelChoiceField(
            required=False,
            queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
            widget=forms.Select(attrs={'class': 'default-select2 form-control producto_nopedido'}),
        )
        self.fields['producto'].empty_label = None
        self.fields['cantidad_presentacion_entrega'] = forms.IntegerField(
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control cantidad_presentacion_entrega_nopedido'})
        )
        self.fields['total_final'] = forms.IntegerField(
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control total_final_nopedido'})
        )


# Sirve para guardar el detallecompra (tanto deseados y no deseados)
class DetalleCompraForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_entrega', 'total_final']

    def __init__(self, *args, **kwargs):
        super(DetalleCompraForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_presentacion_entrega'] = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control cantidad_presentacion_entrega_nopedido'})
        )
        self.fields['total_final'] = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control total_final_nopedido'})
        )


class OrdenCompraConvertirForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrdenCompraConvertirForm, self).__init__(*args, **kwargs)
        self.fields['estado_envio'] = forms.ChoiceField(choices=Compra.ESTADO_ENVIO_CHOICES, widget=forms.Select(
            attrs={'class': 'default-select2 form-control', 'required': 'required'}))
        self.fields['tipo_pago'] = forms.ChoiceField(choices=Compra.TIPO_PAGO_CHOICES, widget=forms.Select(
            attrs={'class': 'default-select2 form-control', 'required': 'required'}))
        self.fields['pago'] = forms.FloatField(required=False,
                                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                               'value': 0}))
        self.fields['tipo_comprobante'] = forms.ModelChoiceField(queryset=TipoComprobante.objects.all(), required=False,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'default-select2 form-control'}))
        self.fields['tipo_comprobante'].empty_label = None
        self.fields['serie_comprobante'] = forms.IntegerField(required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control'}))
        self.fields['numero_comprobante'] = forms.IntegerField(required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control'}))


class OrdenCompraFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrdenCompraFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None
        self.fields['estado'] = forms.ChoiceField(choices=OrdenCompra.ESTADO_CHOICES, required=False,
                                                  widget=forms.SelectMultiple(
                                                      attrs={'class': 'multiple-select2 form-control'}))
