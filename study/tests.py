from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Product, ProductAccess
from study.models import Lesson, LessonView
from study.serializers import LessonSerializer, LessonViewSerializer, LessonUserSerializer


class LessonTestCase(APITestCase):
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

        self.lesson_1 = Lesson.objects.create(title='Lesson_1', video_url='https://localhost', video_duration=100)
        self.lesson_1.products.set([self.product_1, self.product_2])
        self.lesson_2 = Lesson.objects.create(title='Lesson_2', video_url='https://localhost', video_duration=110)
        self.lesson_2.products.set([self.product_3, self.product_4])
        self.lesson_3 = Lesson.objects.create(title='Lesson_3', video_url='https://localhost', video_duration=120)
        self.lesson_3.products.set([self.product_1, self.product_2, self.product_3, self.product_4])
        self.lesson_4 = Lesson.objects.create(title='Lesson_4', video_url='https://localhost', video_duration=105)
        self.lesson_4.products.set([self.product_2, self.product_3, self.product_4])
        self.lesson_5 = Lesson.objects.create(title='Lesson_5', video_url='https://localhost', video_duration=100)
        self.lesson_5.products.set([self.product_1])
        self.lesson_6 = Lesson.objects.create(title='Lesson_6', video_url='https://localhost', video_duration=130)
        self.lesson_6.products.set([self.product_1])

        self.view_u1_l1 = LessonView.objects.create(user=self.test_user_1, lesson=self.lesson_1, lesson_view_during=100)
        self.view_u1_l3 = LessonView.objects.create(user=self.test_user_1, lesson=self.lesson_3, lesson_view_during=110)
        self.view_u1_l5 = LessonView.objects.create(user=self.test_user_1, lesson=self.lesson_5, lesson_view_during=50)

    def test_get_lessons(self):
        self.client.force_login(self.test_user_1)
        url = reverse('lesson-list')
        response = self.client.get(url, format='json')
        serializer = LessonSerializer(Lesson.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_views(self):
        self.client.force_login(self.test_user_1)
        url = reverse('lessonview-list')
        response = self.client.get(url, format='json')
        serializer = LessonViewSerializer(LessonView.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_api_get_user_lessons(self):
        self.client.force_login(self.test_user_1)

        accesses = ProductAccess.objects.filter(user=self.test_user_1, is_valid=True)
        lessons = Lesson.objects.filter(products__in=accesses.values('product_id')).distinct().order_by('id')
        serializer = LessonUserSerializer(lessons, many=True, context={'user': self.test_user_1})

        url = reverse('user-lessons')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

