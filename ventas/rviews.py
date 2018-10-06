from maestro.models import Producto, PresentacionxProducto
from .serializers import PresentacionxProductoSerializer, CatalogoxProveedorSerializer, OfertaVentaSerializer
from rest_framework import generics
from maestro.models import CatalogoxProveedor, PresentacionxProducto
from ventas.models import OfertaVenta
from rest_framework.response import Response


class ProductoDetailsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        presentacionxproducto = PresentacionxProducto.objects.filter(producto__in=self.kwargs['producto']
                                                                     .split(',')).order_by('producto')
        catalogoxproveedor = CatalogoxProveedor.objects.filter(producto__in=self.kwargs['producto']
                                                               .split(',')).order_by('producto')
        ofertaventa = OfertaVenta.objects.filter(producto_oferta__in=self.kwargs['producto']
                                                 .split(','), sucursal=self.kwargs['sucursal']
                                                 ).order_by('producto_oferta')
        context = {
            "request": request,
        }

        presentacionserializer = PresentacionxProductoSerializer(presentacionxproducto, many=True, context=context)
        catalogoserializer = CatalogoxProveedorSerializer(catalogoxproveedor, many=True, context=context)
        ofertaventaserializer = OfertaVentaSerializer(ofertaventa, many=True, context=context)

        response = {'presentacion': presentacionserializer.data, 'precio':  catalogoserializer.data,
                    'oferta': ofertaventaserializer.data}

        return Response(response)
