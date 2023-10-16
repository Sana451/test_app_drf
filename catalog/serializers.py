from django.contrib.auth.models import User
from django.db.models import F, Count, Sum
from rest_framework import serializers

from catalog.models import ProductAccess
from study.models import Product, Lesson, LessonView
from study.serializers import LessonViewSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = '__all__'


class ProductStatSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения статистики по продуктам:
    список всех продуктов на платформе, и по каждому продукту:
    1. Количество просмотренных уроков от всех учеников.
    2. Сколько в сумме все ученики потратили времени на просмотр роликов.
    3. Количество учеников занимающихся на продукте.
    4. Процент приобретения продукта
        (количество полученных доступов к продукту / общее количество пользователей на платформе).
    Увеличивает количество SQL запросов из-за использования SerializerMethodField()
    при сериализации полей lesson_view_count, sum_view_time, total_users_on_product, percent.
    """
    lesson_view_count = serializers.SerializerMethodField()
    sum_view_time = serializers.SerializerMethodField()
    total_users_on_product = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()

    def get_lesson_view_count(self, instance):
        return LessonView.objects.filter(lesson__products=instance, status='VIEWED').count()

    def get_sum_view_time(self, instance):
        qs = LessonView.objects.filter(lesson__products=instance).values('lesson_view_during')
        return sum([i['lesson_view_during'] for i in qs])

    def get_total_users_on_product(self, instance):
        return ProductAccess.objects.filter(product=instance, is_valid=True).count()

    def get_percent(self, instance):
        return round(
            ProductAccess.objects.filter(product=instance, is_valid=True).count() / User.objects.filter(
                is_active=True).count() * 100, 1
        )

    class Meta:
        model = Product
        fields = ['id', 'title', 'lesson_view_count', 'sum_view_time', 'total_users_on_product', 'percent']
        ordering = 'id'


class ProductStatisticSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения статистики по продуктам:
    список всех продуктов на платформе, и по каждому продукту:
    1. Количество просмотренных уроков от всех учеников.
    2. Сколько в сумме все ученики потратили времени на просмотр роликов.
    3. Количество учеников занимающихся на продукте.
    4. Процент приобретения продукта
        (количество полученных доступов к продукту / общее количество пользователей на платформе).
    """
    lesson_view_count = serializers.CharField(default='0')
    sum_view_time = serializers.IntegerField(default=0)
    total_users_on_product = serializers.IntegerField(default=0)
    percent = serializers.FloatField(default=0.0)

    class Meta:
        model = Product
        fields = ['id', 'title', 'lesson_view_count', 'sum_view_time', 'total_users_on_product', 'percent']
        ordering = ['id']
