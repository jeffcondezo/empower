# urls.py
from django.urls import path
from compras.views import OrdenListView, OrdenDetailView, OrdenCreateView, OrdenEditView


urlpatterns = [
    path('orden', OrdenListView.as_view()),
    path('orden/<int:pk>/', OrdenDetailView.as_view()),
    path('orden/<int:pk>/create', OrdenCreateView.as_view()),
    path('orden/<int:pk>/edit', OrdenEditView.as_view()),
]
