# urls.py
from django.urls import path
from ventas.views import OfertaListView, OfertaEditView, OfertaDetailView, VentaListView, VentaCreateView, VentaEditView
from ventas.rviews import ProductoDetailsView

from ventas.views import ticketera

urlpatterns = [
    path('oferta', OfertaListView.as_view()),
    path('oferta/<int:pk>/', OfertaDetailView.as_view()),
    path('oferta/<int:pk>/edit', OfertaEditView.as_view()),
    path('venta', VentaListView.as_view()),
    path('venta/add', VentaCreateView.as_view()),
    path('venta/<int:pk>/edit', VentaEditView.as_view()),

    path('api/productodetails/<str:producto>/<int:sucursal>', ProductoDetailsView.as_view()),

    path('ticket', ticketera)
]
