from django import forms

# Model import-->
from maestro.models import Empresa,Sucursal, Almacen, Categoria, Presentacion, Producto
# Model import<--


class SucursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }


class AlmacenForm(forms.ModelForm):

    class Meta:
        model = Almacen
        fields = '__all__'


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['descripcion', 'padre']


class PresentacionForm(forms.ModelForm):

    class Meta:
        model = Presentacion
        fields = '__all__'


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['descripcion', 'empresa']
