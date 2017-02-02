from rest_framework.serializers import ModelSerializer
from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            #'id',
            'title',
            #'slug',
            'content',
            'timestamp'
        ]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'timestamp'
        ]

class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
    		'user',
            'title',
            'content',
            'slug'
            
        ]
