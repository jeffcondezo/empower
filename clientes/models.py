from django.db import models


# Create your models here.
class Cliente(models.Model):
    TIPO_CHOICES = (
        ('1', 'EMPRESARIAL'),
        ('2', 'PERSONA'),
    )
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default=1)
    documento = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=250)
    ruc = models.CharField(max_length=11, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)
    razon_social = models.CharField(max_length=250, blank=True, null=True)
    nombres = models.CharField(max_length=250, blank=True, null=True)
    apellidos = models.CharField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.descripcion


class ContactosCliente(models.Model):
    nombres = models.CharField(max_length=250)
    apellidos = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    dni = models.CharField(max_length=8, blank=True, null=True)
    cargo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)