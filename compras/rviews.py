from .models import Producto, PresentacionxProducto
from .serializers import ProductoSerializer, PresentacionxProductoSerializer
from rest_framework import generics


class ProductosListView(generics.ListAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        if 'q' in self.request.GET:
            queryset = Producto.objects.filter(descripcion__icontains=self.request.GET['q'])
        else:
            queryset = Producto.objects.all()
        return queryset


class PresentacionxProductoListView(generics.ListAPIView):
    serializer_class = PresentacionxProductoSerializer

    def get_queryset(self):
        queryset = PresentacionxProducto.objects.filter(producto__in=self.kwargs['producto'].split(','))\
            .order_by('producto')
        return queryset
