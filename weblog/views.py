from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from itertools import chain
from rest_framework.response import Response 
from django.db.models import Count
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

from .serializers import PostSerializer, PostCreateSerializer
from .serializers import TagSerializer, CategorySerializer
from .serializers import CommentSerializer, AddCommentSerializer, CommentStatusSerializer
from .models import Post, Tag, Category, Comment
from .pagination import AllArticlesPaginator
from .filters import DateFilter
from .permissions import AuthenticateOwnerPost


class HomeApiView(
                  generics.GenericAPIView):
    
    def get_queryset(self):
        last_six_slider = Post.objects.filter(promote=True)[:6]
        remaining_slider = []
        if last_six_slider.count() < 6:
            remaining_slider = Post.objects.exclude(id__in=[ z.id for z in list(last_six_slider) ]).order_by("-visitors")[:6-last_six_slider.count()]
        slider = list(chain(last_six_slider, remaining_slider))

        lastnews = Post.objects.order_by('-date')[:3]
        return [slider, lastnews]


    queryset = get_queryset(None)
    serializer_class = PostSerializer
    # permission_classes = []

    def get(self, request):
        most_view = Paginator(Post.objects.all().order_by("-visitors"), 6)
        page_number_2 = request.GET.get('page2')
        most_view = most_view.get_page(page_number_2)
        serialize_most_view= PostSerializer(most_view, many=True)
        # paginate_most_view = None
        # serialize_most_view = None
        # page_view = self.request.query_params.get('p1')
        # if page_view is not None:
        #     paginate_most_view = self.paginate_queryset(most_view)
        #     serialize_most_view = self.serializer_class(paginate_most_view, many=True)

        most_comment = Paginator(Post.objects.all().annotate(
            num_comments=Count('comments')).order_by('-num_comments'), 6)
        
        # paginate_most_comment = None
        # serialize_most_comment = None
        # page_comment = self.request.query_params.get('p2')
        # if page_comment is not None:
        #     paginate_most_comment = self.paginate_queryset(most_comment)
        #     serialize_most_comment = self.serializer_class(paginate_most_comment, many=True)
            
        page_number_3 = request.GET.get('page3')
        most_comment = most_comment.get_page(page_number_3)
        serialize_most_comment = PostSerializer(most_comment, many=True)
        # for comment in serialize_most_comment:
        #     comment.append({"true_comment": 22})
        # print(serialize_most_comment)
        # queryset = self.get_queryset()
        serialize_slider = PostSerializer(self.queryset[0], many=True)
        serialize_lastnews = PostSerializer(self.queryset[1], many=True)
        
        return Response({
            "slider": serialize_slider.data,
            "lastnews": serialize_lastnews.data,
            "most-comment": serialize_most_comment.data,
            "most-view": serialize_most_view.data,
        })


class AllArticlesApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = AllArticlesPaginator
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'body']
    filterset_class = DateFilter

    def get_queryset(self):
        queryset = Post.objects.all()

        order_by = self.request.GET.get('order_by')
        if order_by != None and order_by != "":
            order_by = order_by.split(",")

            for item in order_by:
                if item.find("visitors") != -1 or item.find("date") != -1:
                    queryset = queryset.order_by(item)
        
        return queryset


class UserProfileApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = AllArticlesPaginator
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = Post.objects.filter(author = self.request.user)
        return queryset


class CreatePostApiView(generics.ListCreateAPIView,
                        generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCreateSerializer

    def get(self, request):
        categories = Category.objects.all()
        serialize_cat = CategorySerializer(categories, many=True)

        tags = Tag.objects.all()
        serialize_tag = TagSerializer(tags, many=True)

        return Response({
            "category": serialize_cat.data,
            "tag": serialize_tag.data,
        })
        
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    

class DeletePostApiView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          AuthenticateOwnerPost]
    # success_url = reverse_lazy('index')

    def get_queryset(self):
        return Post.objects.all()

class UpdatePostApiView(generics.ListAPIView,
                        generics.UpdateAPIView):
    
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated,
                          AuthenticateOwnerPost]
    
    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs['pk'])
    

class ArticleApiView(APIView):
    serializer_class = PostSerializer

    def get(self, request, pk):
        post_query = get_object_or_404(Post, id=pk)
        post_query.visitors += 1
        post_query.save()
        post_serialize = self.serializer_class(post_query)

        comment_query = Comment.objects.filter(parent__isnull=True, post=post_query, status=True)
        comment_serialize = CommentSerializer(comment_query, many=True)

        return Response({
            "post": post_serialize.data,
            "comment":comment_serialize.data
        })
    

class AddCommentApiView(generics.CreateAPIView):
    serializer_class = AddCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_name = f"{self.request.user.first_name} {self.request.user.last_name}"
        post = Post.objects.get(id=self.kwargs["pk"])
        return serializer.save(name=comment_name, post=post)


class AddSubCommentApiView(generics.CreateAPIView):
    serializer_class = AddCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_name = f"{self.request.user.first_name} {self.request.user.last_name}"
        post = Post.objects.get(id=self.kwargs["pk"])
        parent = Comment.objects.get(id=self.kwargs["id"])
        parent.child.add(serializer.save(name=comment_name, post=post, parent=parent))
        parent.save()


class CheckCommentApiView(generics.GenericAPIView):
    serializer_class = CommentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, AuthenticateOwnerPost]

    def get(self, request, pk):
        comment = self.get_queryset()
        serialize_comment = self.serializer_class(comment, many=True)
        return Response({"comment": serialize_comment.data})
    
    def post(self, request, *args, **kwargs):
        all_status = [request.data['true'],
                      request.data['false'],
                      request.data['delete']]
        all_comments = []

        for i in range(3):
            for comment_id in all_status[i]:
                comment = self.get_object(comment_id)

                if i == 0:
                    comment.status = True
                    comment.save()
                    all_comments.append(comment)

                elif i == 1:
                    comment.status = False
                    comment.save()
                    all_comments.append(comment)

                else:
                    comment.delete()
        
        serialize_comments = self.serializer_class(all_comments, many=True)
        return Response({"comment": serialize_comments.data})

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        queryset = Comment.objects.filter(post=post)
        return queryset
    
    def get_object(self, id):
        try:
            return self.get_queryset().get(id=id)
        
        except(Comment.DoesNotExist):
            return Response({"message": "Access Denied!"},
                             status.HTTP_400_BAD_REQUEST)
        
        
