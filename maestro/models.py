from django.db import models


class Empresa(models.Model):
    descripcion = models.CharField(max_length=150)
    ruc = models.CharField(max_length=11)

    def __str__(self):
        return self.descripcion


class Sucursal(models.Model):
    descripcion = models.CharField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=150)
    responsable = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion


class Categoria(models.Model):
    descripcion = models.CharField(max_length=250)
    nivel = models.SmallIntegerField()
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    padre_total = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='padretotal')

    def __str__(self):
        return self.descripcion


class Almacen(models.Model):
    descripcion = models.CharField(max_length=200)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)


class Producto(models.Model):
    descripcion = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)
    catalogo = models.ManyToManyField(Sucursal)


class Presentacion(models.Model):
    descripcion = models.CharField(max_length=250)


class PresentacionxProducto(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
