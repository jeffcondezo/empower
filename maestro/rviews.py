from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics


class ProductosListView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
