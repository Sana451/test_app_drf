import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product


class Lesson(models.Model):
    title = models.CharField(max_length=30, unique=True)
    products = models.ManyToManyField(Product, related_name='lessons')
    video_url = models.URLField()
    video_duration = models.IntegerField()

    def __str__(self):
        return f"{self.title} => {[i.title for i in self.products.all()]}"


class StatusLesson(models.TextChoices):
    VIEWED = 'VIEWED'
    NOT_VIEWED = 'NOT_VIEWED'


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='views')
    lesson_view_during = models.IntegerField(default=0)
    last_view_datetime = models.DateTimeField(default=django.utils.timezone.now())
    status = models.CharField(max_length=20, choices=StatusLesson.choices, default=StatusLesson.NOT_VIEWED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lesson'], name='user_lesson_unique_constraint'),
        ]

    def __str__(self):
        return f"{self.user} => {self.lesson} {[i for i in self.lesson.products.all()]}"
