# urls.py
from django.urls import path
from ventas.views import OfertaListView, OfertaEditView, OfertaDetailView, VentaListView, VentaCreateView,\
    VentaEditView, VentaDetailView, pruebati
from ventas.rviews import ProductoDetailsView


urlpatterns = [
    path('oferta', OfertaListView.as_view()),
    path('oferta/<int:pk>/', OfertaDetailView.as_view()),
    path('oferta/<int:pk>/edit', OfertaEditView.as_view()),
    path('venta', VentaListView.as_view()),
    path('venta/add', VentaCreateView.as_view()),
    path('venta/<int:pk>/edit', VentaEditView.as_view()),
    path('venta/<int:pk>/', VentaDetailView.as_view()),
    path('ticket', pruebati),

    path('api/productodetails/<str:producto>/<int:sucursal>', ProductoDetailsView.as_view()),

]
