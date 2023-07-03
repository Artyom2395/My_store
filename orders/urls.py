from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, OrederListView, OrderDetailView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_create/order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('', OrederListView.as_view(), name='orders_list'),
    #path('order-canceled/', CanceledView.as_view(), name='order_canceled'),
]
