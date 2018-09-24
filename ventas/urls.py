# urls.py
from django.urls import path
from ventas.views import OfertaListView, OfertaEditView

urlpatterns = [
    path('oferta', OfertaListView.as_view()),
    # path('orden/<int:pk>/', OrdenDetailView.as_view()),
    path('oferta/<int:pk>/edit', OfertaEditView.as_view()),

]
