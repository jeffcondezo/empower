from django import forms

# Model import-->
from django.forms import ModelChoiceField

from maestro.models import Empresa,Sucursal, Almacen, Categoria, Presentacion, Producto, PresentacionxProducto
# Model import<--


class SucursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].empty_label = None


class AlmacenForm(forms.ModelForm):

    class Meta:
        model = Almacen
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AlmacenForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'].empty_label = None


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['descripcion', 'padre']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'padre': forms.Select(attrs={'class': 'default-select2 form-control'})
        }


class PresentacionForm(forms.ModelForm):

    class Meta:
        model = Presentacion
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['descripcion', 'empresa']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].empty_label = None


class ProductoCategoriaForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['categorias']
        widgets = {
            'categorias': forms.SelectMultiple(attrs={'class': 'multiple-select2 form-control'})
        }


class ProductoPresentacionForm(forms.ModelForm):

    class Meta:
        model = PresentacionxProducto
        fields = ['presentacion', 'cantidad']
