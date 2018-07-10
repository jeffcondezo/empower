# urls.py
from django.urls import path
from maestro.views import SucursalListView, SucursalDetailView, SucursalEditView,\
    AlmacenListView, AlmacenDetailView, AlmacenEditView,\
    CategoriaListView, CategoriaDetailView, CategoriaEditView,\
    PresentacionListView, PresentacionDetailView, PresentacionEditView,\
    ProductoListView, ProductoDetailView, ProductoEditView, ProductoCategoriaView, ProductoPresentacionView

urlpatterns = [
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
]
