from django.urls import path, include
from product.views import (
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
    ProductDisableView,
    ExportProductsView,
)


urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('list/', ProductListView.as_view(), name='list'),
    path('disable/<int:pk>/', ProductDisableView.as_view(), name='disable'),
    path('export/products/', ExportProductsView.as_view(), name='export_products'),
]
