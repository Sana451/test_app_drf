from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'accesses', views.ProductAccessViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products-statistic', views.ProductStatisticView.as_view(), name='products-statistic'),
    path('products-stat', views.ProductStatView.as_view(), name='products-stat'),
]
