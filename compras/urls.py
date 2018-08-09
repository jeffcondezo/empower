# urls.py
from django.urls import path
from compras.views import OrdenListView, OrdenDetailView, OrdenCreateView, OrdenEditView
from compras.rviews import ProductosListView, PresentacionxProductoListView, PrecioTentativoView

urlpatterns = [
    path('orden', OrdenListView.as_view()),
    path('orden/<int:pk>/', OrdenDetailView.as_view()),
    path('orden/<int:pk>/create', OrdenCreateView.as_view()),
    path('orden/<int:pk>/edit', OrdenEditView.as_view()),

    path('api/productoxproveedor/<int:proveedor>', ProductosListView.as_view()),
    path('api/presentacionxproducto/<str:producto>', PresentacionxProductoListView.as_view()),
    path('api/preciotentativo/<int:pk>', PrecioTentativoView.as_view()),
]
