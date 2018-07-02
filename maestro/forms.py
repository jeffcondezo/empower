from django import forms

# Model import-->
from maestro.models import Sucursal, Almacen
# Model import<--


class SucursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = '__all__'


class AlmacenForm(forms.ModelForm):

    class Meta:
        model = Almacen
        fields = '__all__'