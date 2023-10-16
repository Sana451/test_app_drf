from django.db.models import Count, Q, F, OuterRef, Sum, Subquery, Case, When, FilteredRelation
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Round

from catalog.models import Product, ProductAccess
from catalog.serializers import ProductSerializer, ProductAccessSerializer, ProductStatisticSerializer, \
    ProductStatSerializer
from study.models import Lesson, LessonView, StatusLesson


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductAccessViewSet(viewsets.ModelViewSet):
    queryset = ProductAccess.objects.all()
    serializer_class = ProductAccessSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductStatView(APIView):
    """
    API для отображения статистики по продуктам:
    список всех продуктов на платформе, и по каждому продукту:
    1. Количество просмотренных уроков от всех учеников.
    2. Сколько в сумме все ученики потратили времени на просмотр роликов.
    3. Количество учеников занимающихся на продукте.
    4. Процент приобретения продукта
        (количество полученных доступов к продукту / общее количество пользователей на платформе).
    28 SQL запросов из-за использования SerializerMethodField()
    при выборке полей lesson_view_count, sum_view_time, total_users_on_product, percent.
    """
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['id']

    def get(self, request):
        qs = Product.objects.all()
        serializer = ProductStatSerializer(qs, many=True)
        return Response(serializer.data)


class ProductStatisticView(APIView):
    """
    API для отображения статистики по продуктам:
    список всех продуктов на платформе, и по каждому продукту:
    1. Количество просмотренных уроков от всех учеников.
    2. Сколько в сумме все ученики потратили времени на просмотр роликов.
    3. Количество учеников занимающихся на продукте.
    4. Процент приобретения продукта
        (количество полученных доступов к продукту / общее количество пользователей на платформе).
    """

    permission_classes = [permissions.IsAuthenticated]
    ordering = ['id']

    def get(self, request):
        total_users_count = User.objects.filter(is_active=True).count()
        products = (Product.objects.annotate(
            total_users_on_product=Count('accesses', filter=Q(accesses__is_valid=True))
        ).annotate(
            percent=Round(F('total_users_on_product') / float(total_users_count) * 100, 1)
        ).annotate(
            sum_view_time=Sum(LessonView.objects.filter(lesson__products=OuterRef('id')).values('lesson_view_during'))
        ).annotate(
            lesson_view_count=Count(
                LessonView.objects.filter(lesson__products=OuterRef('id'),
                                          status=StatusLesson.VIEWED).values('id'))
        ).order_by('id'))

        # products = Product.objects.annotate(
        #     lesson_view_count=Count(
        #         LessonView.objects.filter(
        #             lesson__products=OuterRef('id'),
        #             status=StatusLesson.VIEWED
        #         ).values('id')
        #     ),
        #     sum_view_time=Sum(
        #         LessonView.objects.filter(
        #             lesson__products=OuterRef('id'),
        #         ).values('lesson_view_during')
        #     ),
        #     total_users_on_product=Count(
        #         ProductAccess.objects.filter(product_id=OuterRef('id')).values('id')
        #     ),
        #     percent=F('total_users_on_product') / float(total_users_count) * 100
        # )

        serializer = ProductStatisticSerializer(products, many=True)
        return Response(serializer.data)
