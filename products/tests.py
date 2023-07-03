from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory

# Create your tests here.
class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store')


class ProductListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_list(self):
        path = reverse('products')
        response = self.client.get(path)

        products = Product.objects.all()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['products']), list(products[:3]))

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse('category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        