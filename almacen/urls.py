# urls.py
from django.urls import path
from almacen.views import StockView, KardexView, RecepcionCompraListView, RecepcionCompraEditView,\
    EntregaVentaListView, EntregaVentaEditView

urlpatterns = [
    path('stock/', StockView.as_view()),
    path('kardex/', KardexView.as_view()),
    path('recepcion_compra/', RecepcionCompraListView.as_view()),
    path('recepcion_compra/<int:pk>/', RecepcionCompraEditView.as_view()),
    path('entrega_venta/', EntregaVentaListView.as_view()),
    path('entrega_venta/<int:pk>/', EntregaVentaEditView.as_view()),
]
