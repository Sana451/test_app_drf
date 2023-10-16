from rest_framework import serializers
from study.models import Lesson, LessonView


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = '__all__'


class LessonViewInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выведения статуса и продолжительности
    просмотра урока. Используется в SerializerMethodField()
    при получении поля "lesson_view_info" в LessonUserSerializer.
    """

    class Meta:
        model = LessonView
        fields = ['status', 'lesson_view_during']


class LessonUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выведения списка всех уроков
    по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра.
    Из-за использования SerializerMethodField() количество
    запросов к базе растёт, поэтому реализованы более
    оптимальные LessonUserSerializer2 и LessonUserView2
    """
    lesson_view_info = serializers.SerializerMethodField()

    def get_lesson_view_info(self, instance):
        qs = LessonView.objects.filter(lesson=instance, user=self.context['user'])
        serializer = LessonViewInfoSerializer(qs, many=True)
        return serializer.data

    class Meta:
        model = Lesson
        fields = ["id", "title", "video_duration", "lesson_view_info"]


class LessonUserSerializer2(serializers.ModelSerializer):
    """
    Сериализатор для выведения списка всех уроков
    по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра.
    """
    status = serializers.CharField()
    view_time = serializers.IntegerField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "video_duration", "status", "view_time"]


class LessonProductSerializer(serializers.ModelSerializer):
    """
    API с выведением списка уроков по конкретному продукту к которому
    пользователь имеет доступ, с выведением информации о статусе и времени
    просмотра, а также датой последнего просмотра ролика.
    """
    status = serializers.CharField()
    lesson_view_during = serializers.IntegerField()
    last_view_datetime = serializers.DateTimeField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "video_duration", "status", "lesson_view_during", "last_view_datetime"]
