# urls.py
from django.urls import path
from maestro.views import SucursalListView, SucursalDetailView, SucursalEditView,\
    AlmacenListView, AlmacenDetailView, AlmacenEditView,\
    CategoriaListView, CategoriaDetailView, CategoriaEditView,\
    PresentacionListView, PresentacionDetailView, PresentacionEditView,\
    ProductoListView, ProductoDetailView, ProductoEditView, ProductoCategoriaView, ProductoPresentacionView,\
    CatalogoListView, CatalogoDeleteView, CatalogoAddView,\
    ProveedorListView, ProveedorDetailView, ProveedorEditView,\
    CatalogoProveedorListView, CatalogoProveedorDeleteView, CatalogoProveedorAddView

from maestro.rviews import ProductosListView

from .lviews import AccessView, LoginView, LogoutView, DeniedView

urlpatterns = [
    path('acceso', AccessView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('denied', DeniedView.as_view()),
    path('sucursal/', SucursalListView.as_view()),
    path('sucursal/<int:pk>/', SucursalDetailView.as_view()),
    path('sucursal/<int:pk>/edit', SucursalEditView.as_view()),
    path('almacen/', AlmacenListView.as_view()),
    path('almacen/<int:pk>/', AlmacenDetailView.as_view()),
    path('almacen/<int:pk>/edit', AlmacenEditView.as_view()),
    path('categoria/', CategoriaListView.as_view()),
    path('categoria/<int:pk>/', CategoriaDetailView.as_view()),
    path('categoria/<int:pk>/edit', CategoriaEditView.as_view()),
    path('presentacion/', PresentacionListView.as_view()),
    path('presentacion/<int:pk>/', PresentacionDetailView.as_view()),
    path('presentacion/<int:pk>/edit', PresentacionEditView.as_view()),
    path('producto/', ProductoListView.as_view()),
    path('producto/<int:pk>/', ProductoDetailView.as_view()),
    path('producto/<int:pk>/edit', ProductoEditView.as_view()),
    path('producto/<int:pk>/categoria', ProductoCategoriaView.as_view()),
    path('producto/<int:pk>/presentacion', ProductoPresentacionView.as_view()),
    path('catalogo/', CatalogoListView.as_view()),
    path('catalogo/delete', CatalogoDeleteView.as_view()),
    path('catalogo/add/<int:pk>/', CatalogoAddView.as_view()),
    path('proveedor/', ProveedorListView.as_view()),
    path('proveedor/<int:pk>/', ProveedorDetailView.as_view()),
    path('proveedor/<int:pk>/edit', ProveedorEditView.as_view()),
    path('catalogoproveedor/', CatalogoProveedorListView.as_view()),
    path('catalogoproveedor/delete', CatalogoProveedorDeleteView.as_view()),
    path('catalogoproveedor/add/<int:pk>/', CatalogoProveedorAddView.as_view()),
    # API URL'S
    path('api/producto', ProductosListView.as_view()),
]
