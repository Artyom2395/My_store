from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductsListView.as_view(), name='products'),
    path('products/category/<int:category_id>/', views.ProductsListView.as_view(), name='category'),
    path('products/page/<int:page>/', views.ProductsListView.as_view(), name='paginator'),
    path('products/baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('products/baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]