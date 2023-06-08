from rest_framework import serializers
from rest_framework import pagination
from rest_framework.fields import CurrentUserDefault

from .models import Post, Comment, Tag, Category

class PostSerializer(serializers.ModelSerializer):

    count_comments = serializers.IntegerField(source="true_comment_count", read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'date', 'visitors', 'body', 'author', 'tags', 'category', 'promote', 'count_comments')

class PostCreateSerializer(serializers.ModelSerializer):
    
    # author = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'category', 'promote', 'author')
    
    # def save(self):
    #     title = self.validated_data("title")
    #     image = self.validated_data("image")
    #     body = self.validated_data("body")
    #     tags = self.validated_data("tags")
    #     category = self.validated_data("category")
    #     promote = self.validated_data("promote")
    #     date = self.validated_data("date")
    #     author = CurrentUserDefault


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('name', 'text', 'date_added', 'child')