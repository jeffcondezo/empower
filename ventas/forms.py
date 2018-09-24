from django import forms
from django.forms import ModelChoiceField

# Model import-->
from ventas.models import OfertaVenta
# Model import<--


class OfertaVentaForm(forms.ModelForm):

    class Meta:
        model = OfertaVenta
        fields = ['sucursal', 'tipo', 'tipo_duracion', 'producto_oferta',
                  'presentacion_oferta', 'cantidad_oferta', 'producto_retorno',
                  'presentacion_retorno', 'retorno', 'fechahora_inicio', 'fechahora_fin', 'stock_limite']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'tipo_duracion': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'producto_oferta': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'presentacion_oferta': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'cantidad_oferta': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto_retorno': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'presentacion_retorno': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'retorno': forms.NumberInput(attrs={'class': 'form-control'}),
            'fechahora_inicio': forms.TextInput(attrs={'class': 'form-control'}),
            'fechahora_fin': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_limite': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OfertaVentaForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'].empty_label = None
        self.fields['tipo'].empty_label = None
        self.fields['tipo_duracion'].empty_label = None
        self.fields['producto_oferta'].empty_label = None
        self.fields['presentacion_oferta'].empty_label = None
        self.fields['producto_retorno'].empty_label = None
        self.fields['presentacion_retorno'].empty_label = None
