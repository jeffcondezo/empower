# urls.py
from django.urls import path
from compras.views import OrdenListView, OrdenDetailView


urlpatterns = [
    path('orden', OrdenListView.as_view()),
    path('orden/<int:pk>/', OrdenDetailView.as_view()),

]
