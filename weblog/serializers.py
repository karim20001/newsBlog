from rest_framework import serializers
from rest_framework import pagination

from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    comments = serializers.IntegerField(source="true_comment_count", read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'date', 'visitors', 'body', 'author', 'tags', 'category', 'promote', 'comments')

# class PaginatorPostSerializer(pagination.PageNumberPagination):
#     class Meta:
#         object_serializer_class = PostSerializer
