from django import forms

# Model import-->
from django.forms import ModelChoiceField

from clientes.models import Cliente
# Model import<--


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['tipo', 'telefono', 'correo']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].empty_label = None
