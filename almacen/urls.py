# urls.py
from django.urls import path
from almacen.views import StockView, KardexView

urlpatterns = [
    path('stock/', StockView.as_view()),
    path('kardex/', KardexView.as_view()),
]
