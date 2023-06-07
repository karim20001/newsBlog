from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from itertools import chain
from rest_framework.response import Response 
from django.db.models import Count
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import PostSerializer
from .models import Post
from .pagination import AllArticlesPaginator
from .filters import DateFilter


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
        most_view = Paginator(Post.objects.all().order_by("-visitors"), 1)
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
            num_comments=Count('comments')).order_by('-num_comments'), 1)
        
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
    filter_backends = [DjangoFilterBackend]
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
    