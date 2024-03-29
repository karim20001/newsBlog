from django.urls import path, include
from rest_framework.routers import DefaultRouter
from weblog import views

router = DefaultRouter()
# router.register('', views.HomeApiView, basename="home")

urlpatterns = [
    # path('', include(router.urls)),
    path('', views.HomeApiView.as_view(), name="home"),
    path('all-articles/', views.AllArticlesApiView.as_view(), name="all-articles"),
    path('article/<int:pk>', views.ArticleApiView.as_view(), name="article"),
    path('profile/', views.UserProfileApiView.as_view(), name="profile"),
    path('profile/create-post', views.CreatePostApiView.as_view(), name="profile"),
    path('profile/delete-post/<int:pk>', views.DeletePostApiView.as_view()),
    path('profile/update-post/<int:pk>', views.UpdatePostApiView.as_view()),
    path('article/<int:pk>/add-comment', views.AddCommentApiView.as_view()),
    path('article/<int:pk>/<int:id>/add-subcomment', views.AddSubCommentApiView.as_view()),
    path('profile/<int:pk>/comments/', views.CheckCommentApiView.as_view(), name="check-comment"),
]
