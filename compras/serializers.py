from maestro.models import Producto, PresentacionxProducto, Presentacion
from rest_framework import serializers


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id', 'descripcion']


class PresentacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentacion
        fields = ['id', 'descripcion']


class PresentacionxProductoSerializer(serializers.ModelSerializer):
    presentacion = PresentacionSerializer()

    class Meta:
        model = PresentacionxProducto
        fields = ['id', 'presentacion', 'producto']