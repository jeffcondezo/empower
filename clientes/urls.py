# urls.py
from django.urls import path
from clientes.views import ClienteListView

from maestro.rviews import ProductosListView


urlpatterns = [
    path('cliente/', ClienteListView.as_view()),
    # path('sucursal/<int:pk>/', SucursalDetailView.as_view()),
    # path('sucursal/<int:pk>/edit', SucursalEditView.as_view()),
    # API URL'S
    path('api/producto', ProductosListView.as_view()),
]
