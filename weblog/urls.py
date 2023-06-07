from django.urls import path, include
from rest_framework.routers import DefaultRouter
from weblog import views

router = DefaultRouter()
# router.register('', views.HomeApiView, basename="home")

urlpatterns = [
    # path('', include(router.urls)),
    path('', views.HomeApiView.as_view(), name="home"),
    path('all-articles/', views.AllArticlesApiView.as_view(), name="all-articles"),
]
