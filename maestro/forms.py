from django import forms

# Model import-->
from maestro.models import Sucursal, Almacen, Categoria, Presentacion
# Model import<--


class SucursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = '__all__'


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
