# urls.py
from django.urls import path
from compras.views import CompraListView, CompraCreateView, CompraEditView
from compras.rviews import ProductosListView, PresentacionxProductoListView, PrecioTentativoView

urlpatterns = [
    path('compra', CompraListView.as_view()),
    path('compra/add', CompraCreateView.as_view()),
    path('compra/<int:pk>/edit', CompraEditView.as_view()),

    path('api/productoxproveedor/<int:proveedor>', ProductosListView.as_view()),
    path('api/presentacionxproducto/<str:producto>', PresentacionxProductoListView.as_view()),
    path('api/preciotentativo/<int:pk>', PrecioTentativoView.as_view()),
]
