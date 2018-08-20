# urls.py
from django.urls import path
from almacen.views import StockView, KardexView, OrdenListView,  OrdenDetailView

urlpatterns = [
    path('stock/', StockView.as_view()),
    path('kardex/', KardexView.as_view()),
    path('ordencompra/', OrdenListView.as_view()),
    path('ordencompra/<int:pk>/recepcion', OrdenDetailView.as_view()),
]
