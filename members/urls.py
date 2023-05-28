from django.urls import include, path
from rest_framework import routers

from members import views

router = routers.DefaultRouter()
# router.register('sign-up', views.UserSignUpViewSet, basename='sign-up')

urlpatterns = [
    path('', include(router.urls)),
    path('sign-up/', views.UserSignUpViewSet.as_view(), name='sign-up'),
    path('sign-in/', views.UserLoginApiView.as_view()),
]


