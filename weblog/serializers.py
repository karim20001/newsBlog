from rest_framework import serializers
from rest_framework import pagination
from rest_framework.fields import CurrentUserDefault

from .models import Post, Comment, Tag, Category

class PostSerializer(serializers.ModelSerializer):

    count_comments = serializers.IntegerField(source="true_comment_count", read_only=True)
    author_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'date', 'visitors', 'body', 'author_name', 'tags', 'category', 'promote', 'count_comments')
        depth = 1

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
    # child_comment = ChildCommentSerializer(read_only=True, many=True)
    # child_comment = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('name', 'text', 'date_added', 'child')
        depth = 1
    
    
    # def get_child_comment(self, obj):
    #     child_comment = Comment.objects.filter(id__in=obj.child)
    #     return ChildCommentSerializer(child_comment, many=True).data


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text',)


class CommentStatusSerializer(serializers.ModelSerializer):
    parent_name = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields= ('name', 'text', 'parent_name', 'status',)
        depth = 1