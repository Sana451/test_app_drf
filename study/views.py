from django.db.models import F, FilteredRelation, Q
from rest_framework import viewsets, exceptions
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.models import ProductAccess
from study.models import Lesson, LessonView
from study.serializers import LessonSerializer, LessonViewSerializer, LessonUserSerializer, LessonProductSerializer, \
    LessonUserSerializer2


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewsViewSet(viewsets.ModelViewSet):
    queryset = LessonView.objects.all()
    serializer_class = LessonViewSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonUserView(APIView):
    """
    View для выведения списка всех уроков по всем продуктам
    к которым пользователь имеет доступ, с выведением информации
    о статусе и времени просмотра. Из-за использования в сериализаторе
    SerializerMethodField() количество запросов к базе растёт,
    поэтому реализованы более оптимальные LessonUserSerializer2 и
    LessonUserView2.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accesses = ProductAccess.objects.filter(user=request.user, is_valid=True)
        lessons = Lesson.objects.filter(products__in=accesses.values('product_id')).distinct().order_by('id')
        serializer = LessonUserSerializer(lessons, many=True, context={'user': request.user})
        return Response(serializer.data)


class LessonUserView2(APIView):
    """
    API для выведения списка всех уроков по всем продуктам
    к которым пользователь имеет доступ, с выведением информации
    о статусе и времени просмотра (3 SQl запроса вместо 10 в
    LessonUserView)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accesses = ProductAccess.objects.filter(user=request.user, is_valid=True)
        lessons = Lesson.objects.filter(products__in=accesses.values('product_id')).distinct().alias(
            lesson_view_info=FilteredRelation('views', condition=Q(views__user=self.request.user))
        ).annotate(
            status=F('lesson_view_info__status'),
            view_time=F('lesson_view_info__lesson_view_during')
        ).order_by('id')

        serializer = LessonUserSerializer2(lessons, many=True)
        return Response(serializer.data)


class LessonProductView(APIView):
    """
    API с выведением списка уроков по конкретному продукту к которому
    пользователь имеет доступ, с выведением информации о статусе и времени
    просмотра, а также датой последнего просмотра ролика. Только 4 SQL запроса.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        accesses = ProductAccess.objects.filter(user=request.user, is_valid=True)

        if not (product_id in accesses.values_list('product_id', flat=True)):
            raise exceptions.NotFound
        lessons = Lesson.objects.filter(products=product_id).distinct().annotate(
            status=F('views__status'),
            lesson_view_during=F("views__lesson_view_during"),
            last_view_datetime=F('views__last_view_datetime')
        )

        serializer = LessonProductSerializer(lessons, many=True, context={'user': request.user})
        return Response(serializer.data)
