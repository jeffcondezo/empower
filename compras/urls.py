# urls.py
from django.urls import path
from compras.views import CompraListView, CompraCreateView, CompraEditView, CompraDetailView,\
    reporte_orden, CompraEntregaView, CompraCancelarView, NotaCreditoListView, NotaCreditoDetailView,\
    DetalleNotaCreditoConsignaView, NotaCreditoCerrarView
from compras.rviews import ProductosListView, PresentacionxProductoListView, PrecioTentativoView
app_name = 'compras'

urlpatterns = [
    path('compra', CompraListView.as_view()),
    path('compra/add', CompraCreateView.as_view()),
    path('compra/<int:pk>/edit', CompraEditView.as_view()),
    path('compra/<int:compra>/entrega', CompraEntregaView.as_view()),
    path('compra/<int:compra>/cancelar', CompraCancelarView.as_view()),
    path('compra/<int:pk>/', CompraDetailView.as_view()),
    path('notacredito', NotaCreditoListView.as_view()),
    path('notacredito/<int:pk>/', NotaCreditoDetailView.as_view()),
    path('notacredito/<int:pk>/cerrar', NotaCreditoCerrarView.as_view()),
    path('detallenotacredito/<int:detalle_notacredito>/consignar', DetalleNotaCreditoConsignaView.as_view()),
    path('reporteorden/', reporte_orden, name='reporteorden'),

    path('api/productoxproveedor/<int:proveedor>', ProductosListView.as_view()),
    path('api/presentacionxproducto/<str:producto>', PresentacionxProductoListView.as_view()),
    path('api/preciotentativo/<int:pk>', PrecioTentativoView.as_view()),
]
