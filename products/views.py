from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.models import Product, ProductCategory, Basket

# Create your views here.
class IndexView(TemplateView):
    template_name = 'products/index.html'
    #Если контекст str
    extra_context = {'title': 'Store',}

class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    #Фильтрация по категориям Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    def get_queryset(self) -> QuerySet[Any]:
        #Это Product.objects.all() все объекты
        queryset = super(ProductsListView, self).get_queryset()
        #Достаем информацию, кт пришла в urls
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

@login_required    
def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.quantity > 0:
        product.quantity -= 1
        product.save()
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required 
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    product = basket.product
    product.quantity += 1
    product.save()
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))