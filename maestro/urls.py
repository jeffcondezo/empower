# urls.py
from django.urls import path
from maestro.views import SucursalListView, SucursalDetailView, SucursalEditView,\
    AlmacenListView, AlmacenDetailView, AlmacenEditView

urlpatterns = [
    path('sucursal/', SucursalListView.as_view()),
    path('sucursal/<int:pk>/', SucursalDetailView.as_view()),
    path('sucursal/<int:pk>/edit', SucursalEditView.as_view()),
    path('almacen/', AlmacenListView.as_view()),
    path('almacen/<int:pk>/', AlmacenDetailView.as_view()),
    path('almacen/<int:pk>/edit', AlmacenEditView.as_view()),
]
