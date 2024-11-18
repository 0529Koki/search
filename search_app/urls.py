from django.urls import path
from .views import ProductSearchAPI

urlpatterns = [
    path('api/search/', ProductSearchAPI.as_view(), name='product-search-api'),
    path('api/amazon-search/', amazon_product_search_view, name='amazon- search'),
]
