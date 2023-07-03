from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order

# Create your views here.
class OrederListView(ListView):
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(OrederListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)

class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ № {self.object.id}'
        return context

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    
class CanceledView(TemplateView):
    template_name = 'oreders/canceled.html'

class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = 'order-success/'
    extra_context = {'title': 'Оформление заказа',}

    #Чтобы заказ подтягивался под того, кто создал, сохранял в данные из формы
    def form_valid(self, form):
        baskets = Basket.objects.filter(user=self.request.user)
        form.instance.status = form.instance.PAID
        form.instance.basket_history = {
           'purchased_items': [basket.de_json() for basket in baskets],
           'total_sum': float(baskets.total_sum()),
       }
        baskets.delete()
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
   

   