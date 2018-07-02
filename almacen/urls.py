# urls.py
from django.urls import path
from almacen.views import StockView

urlpatterns = [
    path('stock/', StockView.as_view()),
]
