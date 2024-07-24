# urls.py
from django.urls import path
from .views import CartaoCreateView, CartaoListView,UploadCartaoFileView, CartaoSearchView

urlpatterns = [
    path('create/', CartaoCreateView.as_view(), name='cartao_create'),
    path('', CartaoListView.as_view(), name='cartao_list'),
    path('upload/', UploadCartaoFileView.as_view(), name='cartao_upload'),
    path('search/<str:numero>/', CartaoSearchView.as_view(), name='search_cartao'),
]
