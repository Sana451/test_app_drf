from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Product, ProductAccess
from catalog.serializers import ProductSerializer, ProductAccessSerializer


class CatalogTestCase(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user('owner_user')
        self.test_user_1 = User.objects.create_user('test_user_1')
        self.test_user_2 = User.objects.create_user('test_user_2')
        self.test_user_3 = User.objects.create_user('test_user_3')
        self.test_user_4 = User.objects.create_user('test_user_4')

        self.product_1 = Product.objects.create(title='Product_1', owner=self.owner_user)
        self.product_2 = Product.objects.create(title='Product_2', owner=self.owner_user)
        self.product_3 = Product.objects.create(title='Product_3', owner=self.owner_user)
        self.product_4 = Product.objects.create(title='Product_4', owner=self.owner_user)

        self.access_u1_pr1 = ProductAccess.objects.create(user=self.test_user_1, product=self.product_1, is_valid=True)
        self.access_u1_pr2 = ProductAccess.objects.create(user=self.test_user_1, product=self.product_2, is_valid=True)
        self.access_u1_pr3 = ProductAccess.objects.create(user=self.test_user_1, product=self.product_3, is_valid=True)
        self.access_u1_pr4 = ProductAccess.objects.create(user=self.test_user_1, product=self.product_4, is_valid=True)

    def test_get_products(self):
        self.client.force_login(self.test_user_1)
        serializer = ProductSerializer(Product.objects.all(), many=True)
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_accesses_to_product(self):
        self.client.force_login(self.test_user_1)
        serializer = ProductAccessSerializer(ProductAccess.objects.all(), many=True)
        url = reverse('productaccess-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)


