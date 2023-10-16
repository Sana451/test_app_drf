from django.urls import path

from . import views

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'lessons', views.LessonViewSet)
router.register(r'views', views.LessonViewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-lessons', views.LessonUserView.as_view(), name='user-lessons'),
    path('user-lessons2', views.LessonUserView2.as_view(), name='user-lessons2'),
    path('user-products/<int:product_id>/lessons', views.LessonProductView.as_view(), name='user-products-lessons'),
]
